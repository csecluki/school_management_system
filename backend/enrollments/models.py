from django.db import models
from django.core.exceptions import ValidationError

from users.models import User
from courses.models import CourseGroup


class RecruitmentStrategy(models.Model):

    STRATEGY_CHOICES = [
        (0, 'First in first served'),
        (1, 'Manual'),
    ]

    id = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, primary_key=True)
    is_auto_triggered = models.BooleanField()

    class Meta:
        default_permissions = ()

    def execute_acceptance_logic(self, group_enrollment, final=False):
        if not final and not self.is_auto_triggered:
            return False
        match self.id:
            case 0:
                self.first_in_first_served(group_enrollment)
            case 1:
                self.manual(group_enrollment)
    
    def first_in_first_served(self, group_enrollment):
        free_spots = group_enrollment.max_students - group_enrollment.group.students.count()
        for application in group_enrollment.student_applications.all():
            if application.status == 0 and free_spots > 0:
                application.accept()
                group_enrollment.group.add_student(application.student)
    
    def manual(self, group_enrollment):
        for application in group_enrollment.student_applications.filter(status=1):
            group_enrollment.group.add_student(application.student)


class GroupEnrollment(models.Model):
    
    group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='enrollments')
    max_students = models.PositiveSmallIntegerField()
    recruitment_strategy = models.OneToOneField(RecruitmentStrategy, on_delete=models.CASCADE)
    
    @property
    def is_active(self):
        return self.enrollment.is_active and not self.limit_reached

    @property
    def limit_reached(self):
        return self.group.students.count() >= self.max_students
    
    @property
    def applications_count(self):
        return self.student_applications.count()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.enrollment.is_active:
            raise ValidationError({'error': 'Enrollment is not active. '})
        if self.enrollment.period != self.group.period:
            raise ValidationError({'error': 'Enrollment has other Period than GroupTimeTable. '})
        if GroupEnrollment.objects.filter(
            group=self.group,
            enrollment=self.enrollment
        ).exists():
            raise ValidationError({'error': 'Enrollment for this group already exists. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def trigger_recruitment_strategy(self):
        return self.recruitment_strategy.execute_acceptance_logic(self)
    
    def resolve(self):
        return self.recruitment_strategy.execute_acceptance_logic(final=True)


class StudentEnrollment(models.Model):
    
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'accepted'),
        (2, 'rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    group_enrollment = models.ForeignKey(GroupEnrollment, on_delete=models.CASCADE, related_name='student_applications')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.student.groups.filter(name="Students").exists():
            raise ValidationError({'error': 'Chosen user is not a student. '})
        
        if self.group_enrollment.group.students.filter(id=self.student.id).exists():
            raise ValidationError({'error': "Student already in class. "})
        
        if self.group_enrollment.limit_reached:
            raise ValidationError({'error': "There are no available spots in this class. "})
        
        last_request = self.get_last_student_enrollment_for_group(self)
        if self.status == 0 and last_request:
            raise ValidationError({'error': f"Application already sent, status: {last_request.get_status_display()}. "})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = 0
        self.clean()
        super().save(*args, **kwargs)
        self.group_enrollment.trigger_recruitment_strategy()
    
    def accept(self):
        self.status = 1
        self.save()
    
    def reject(self):
        self.status = 2
        self.save()
    
    def get_last_student_enrollment_for_group(self, instance):
        return StudentEnrollment.objects.filter(
            student=instance.student,
            group_enrollment=instance.group_enrollment
        ).order_by('-update_date').first()
