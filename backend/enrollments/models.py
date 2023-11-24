from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import User
from timetables.models import CourseTimeTable, Period


class RecruitmentStrategy(models.Model):

    STRATEGY_CHOICES = [
        (0, 'First in first served'),
        (1, 'Manual'),
    ]

    id = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, primary_key=True)
    is_auto_triggered = models.BooleanField()

    def execute_acceptance_logic(self, course_enrollment, final=False):
        if not final and not self.is_auto_triggered:
            return False
        match self.id:
            case 0:
                self.first_in_first_served(course_enrollment)
            case 1:
                self.manual(course_enrollment)
    
    def first_in_first_served(self, course_enrollment):
        free_spots = course_enrollment.max_students - course_enrollment.course.students.count()
        for application in course_enrollment.student_applications.all():
            if application.status == 0 and free_spots > 0:
                application.accept()
                course_enrollment.course.add_student(application.student)
    
    def manual(self, course_enrollment):
        for application in course_enrollment.student_applications.filter(status=1):
            course_enrollment.course.add_student(application.student)


class Enrollment(models.Model):

    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def is_active(self):
        return self.start_date <= timezone.localdate() <= self.end_date

    class Meta:
        default_permissions = ()

    def clean(self):
        if timezone.localdate() > self.period.end_date:
            raise ValidationError({'error': "Can't create enrollment for ended Period. "})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CourseEnrollment(models.Model):
    
    course = models.ForeignKey(CourseTimeTable, on_delete=models.CASCADE, related_name='enrollments')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='courses')
    max_students = models.PositiveSmallIntegerField()
    recruitment_strategy = models.OneToOneField(RecruitmentStrategy, on_delete=models.CASCADE)

    @property
    def limit_reached(self):
        return self.course.students.count() >= self.max_students
    
    @property
    def is_active(self):
        return self.enrollment.is_active and not self.limit_reached
    
    @property
    def applications_count(self):
        return self.student_applications.count()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if CourseEnrollment.objects.filter(
            course=self.course,
            enrollment=self.enrollment
        ).exists():
             raise ValidationError({'error': 'Enrollment for this course already exists. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def trigger_recruitment_strategy(self):
        return self.recruitment_strategy.execute_acceptance_logic(self)
    
    def resolve_recruitment(self):
        return self.recruitment_strategy.execute_acceptance_logic(final=True)


class StudentEnrollment(models.Model):
    
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'accepted'),
        (2, 'rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course_enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='student_applications')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.student.groups.filter(name="Students").exists():
            raise ValidationError({'error': 'Chosen user is not a student. '})
        
        if self.course_enrollment.course.students.filter(id=self.student.id).exists():
            raise ValidationError({'error': "Student already in class. "})
        
        if self.course_enrollment.limit_reached:
            raise ValidationError({'error': "There are no available spots in this class. "})
        
        last_request = self.get_last_student_enrollment_for_course(self)
        if self.status == 0 and last_request:
            raise ValidationError({'error': f"Application already sent, status: {last_request.get_status_display()}. "})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 0
        self.clean()
        super().save(*args, **kwargs)
        self.course_enrollment.trigger_recruitment_strategy()
    
    def accept(self):
        self.status = 1
        self.save()
    
    def reject(self):
        self.status = 2
        self.save()
    
    def get_last_student_enrollment_for_course(self, instance):
        return StudentEnrollment.objects.filter(
            student=instance.student,
            course_enrollment=instance.course_enrollment
        ).order_by('-update_date').first()
