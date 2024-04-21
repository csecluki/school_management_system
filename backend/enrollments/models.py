from django.db import models
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from statistics import mean

from .managers import EnrollmentManager, EnrollmentPhaseManager, GroupEnrollmentManager, StudentEnrollmentManager
from .validators import full_minutes, step_5_min
from users.models import User
from courses.models import CourseGroup
from grades.models import EndGrade


class RecruitmentStrategy(models.Model):

    STRATEGY_CHOICES = [
        (0, 'First in first served'),
        (1, 'Manual'),
        (2, 'Highest endgrade average')
    ]

    id = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, primary_key=True)
    is_auto_accepted = models.BooleanField(default=0)
    is_manual_accept = models.BooleanField(default=0)

    class Meta:
        default_permissions = ()

    def resolve_group_enrollment(self, group_enrollment: 'GroupEnrollment'):
        if self.id == 0:
            pass
        if self.id == 1:
            # todo: send notification to teacher
            pass
        if self.id == 2:
            self.highest_endgrade_average(group_enrollment)
    
    def highest_endgrade_average(self, group_enrollment: 'GroupEnrollment'):
        applications = group_enrollment.student_applications.exclude(Q(status=3) | Q(joined=True))
        limit = group_enrollment.max_students - group_enrollment.student_applications.filter(joined=True).count()
        ranking = {
            application.student: self.calculate_average(EndGrade.objects.get_student_endgrades(application.student))
            for application in applications
        }
        winners = [student for student, _ in sorted(ranking.items(), key=lambda x: -x[1])][:limit]
        accepted = applications.filter(student__in=winners)
        rejected = applications.exclude(student__in=winners)
        for student_enrollment in accepted:
            student_enrollment.accept()
        for student_enrollment in rejected:
            student_enrollment.reject()

    def calculate_average(self, data):
        return mean(x['endgrade'] for x in data)


class Enrollment(models.Model):

    title = models.CharField(max_length=64, unique=True)
    
    @property
    def is_active(self):
        now = timezone.now()
        return self.first_phase.start_date <= now <= self.last_phase.decision_deadline
    
    @property
    def can_apply(self):
        return any(phase.can_apply for phase in self.phases.all())
    
    @property
    def can_join(self):
        return any(phase.can_join for phase in self.phases.all())
    
    @property
    def first_phase(self):
        return self.phases.order_by('start_date').first()

    @property
    def last_phase(self):
        return self.phases.order_by('-start_date').first()
    
    objects = EnrollmentManager()

    class Meta:
        default_permissions = ()
    
    def get_active_phase(self):
        now = timezone.now()
        return self.phases.filter(Q(decision_deadline__gte=now) & Q(start_date__lte=now))


class EnrollmentPhase(models.Model):

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='phases')
    start_date = models.DateTimeField(validators=[step_5_min, full_minutes])
    application_deadline = models.DateTimeField(validators=[step_5_min, full_minutes])
    decision_deadline = models.DateTimeField(validators=[step_5_min, full_minutes])

    @property
    def is_active(self):
        return self.start_date <= timezone.now() <= self.decision_deadline

    @property
    def can_apply(self):
        return self.start_date <= timezone.now() <= self.application_deadline

    @property
    def can_join(self):
        return self.application_deadline <= timezone.now() <= self.decision_deadline
    
    @property
    def is_first(self):
        return self == self.enrollment.phases.order_by('start_date').first()
    
    @property
    def is_last(self):
        return self == self.enrollment.phases.order_by('-start_date').first()
    
    objects = EnrollmentPhaseManager()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.start_date < self.application_deadline < self.decision_deadline:
            raise ValidationError(detail="Datetime fields should be in order: start_date < application_deadline < decision_deadline. ")
        enrollment_stages = EnrollmentPhase.objects.filter(enrollment=self.enrollment).order_by('start_date')
        if self.id:
            enrollment_stages = enrollment_stages.exclude(id=self.id)
        check = enrollment_stages.filter(Q(decision_deadline__lte=self.start_date) | Q(start_date__gte=self.decision_deadline))
        if [x.id for x in check] != [x.id for x in enrollment_stages]:
            raise ValidationError(detail="Phase doesn't fit enrollment structure. ")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class GroupEnrollment(models.Model):

    STATUS = [
        (0, 'created'),
        (1, 'open'),
        (2, 'closed'),
        (3, 'cancelled'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='group_enrollments')
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='enrollments')
    max_students = models.PositiveSmallIntegerField()
    recruitment_strategy = models.ForeignKey(RecruitmentStrategy, on_delete=models.CASCADE, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    min_students = models.PositiveSmallIntegerField(default=1)

    @property
    def is_auto_accepting_application(self):
        return self.recruitment_strategy.is_auto_accepted

    @property
    def manual_accept_available(self):
        return self.recruitment_strategy.is_manual_accept

    @property
    def limit_reached(self) -> bool:
        return self.course_group.students.count() >= self.max_students
    
    @property
    def applications_count(self) -> int:
        return self.student_applications.count()
    
    @property
    def can_apply(self):
        return not self.limit_reached and self.status == 1 and self.enrollment.can_apply
    
    @property
    def can_join(self):
        return not self.limit_reached and self.status == 1 and self.enrollment.can_join
    
    objects = GroupEnrollmentManager()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.pk:
            if GroupEnrollment.objects.filter(
                course_group=self.course_group
            ).exists():
                raise ValidationError(detail='Enrollment for this course_group already exists. ')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def trigger_recruitment_strategy(self, student_enrollment: 'StudentEnrollment'):
        return self.recruitment_strategy.resolve_student_enrollment(student_enrollment)
    
    def resolve(self):
        return self.recruitment_strategy.resolve_group_enrollment(self)
    
    def reject_all_unaccepted_student_enrollments(self):
        self.student_applications.filter(status=0).update(status=2)
    
    def deny_accepted_student_enrollments_not_joined(self):
        self.student_applications.filter(Q(status=1) & Q(joined=False)).update(status=3)
    
    def reject_all_student_enrollments(self):
        self.student_applications.update(status=2)
    
    def make_pending_from_rejected(self):
        self.student_applications.filter(status=2).update(status=0)
    
    def open(self):
        if self.status != 0:
            raise ValidationError(detail=f"Can't open {self.get_status_display()} enrollment. ")
        self.status = 1
        self.save()
    
    def close(self, limit_reached=False, last_phase=False, force=False):
        if self.status != 1:
            raise ValidationError(detail=f"Can't close {self.get_status_display()} enrollment. ")
        if force:
            self.reject_all_student_enrollments()
            self.status = 2
        elif limit_reached or last_phase:
            self.deny_accepted_student_enrollments_not_joined()
            self.status = 2
        elif not last_phase:
            self.deny_accepted_student_enrollments_not_joined()
            self.make_pending_from_rejected()
        self.save()
    
    def cancel(self):
        if self.status == 3:
            raise ValidationError(detail=f"Can't cancel {self.get_status_display()} enrollment. ")
        self.reject_all_student_enrollments()
        self.course_group.remove_students()
        self.status = 3
        self.save()
    
    def add_student_to_group(self, student):
        self.course_group.add_student(student)
        if self.limit_reached:
            self.close(limit_reached=True)


class StudentEnrollment(models.Model):
    
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'accepted'),
        (2, 'rejected'),
        (3, 'denied'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    group_enrollment = models.ForeignKey(GroupEnrollment, on_delete=models.CASCADE, related_name='student_applications')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    joined = models.BooleanField(default=False)
    update_date = models.DateTimeField(auto_now=True)

    @property
    def manual_accept_available(self):
        return self.group_enrollment.manual_accept_available

    objects = StudentEnrollmentManager()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.group_enrollment.can_apply:
            raise ValidationError(detail="Enrollment isn't open for this group. ")
        if not self.student.groups.filter(name="Students").exists():
            raise ValidationError(detail='Chosen user is not a student. ')
        if StudentEnrollment.objects.has_student_pending_request_to_group(self.student, self.group_enrollment):
            raise ValidationError(detail=f"Application already sent. ")
    
    def save(self, *args, **kwargs):
        auto_accept = False
        if not self.pk:
            self.clean()
            self.enrollment_phase = self.group_enrollment.enrollment.get_active_phase()
            auto_accept = self.group_enrollment.is_auto_accepting_application
        super().save(*args, **kwargs)
        if auto_accept:
            self.accept(auto_join=True)
    
    def accept(self, auto_join=False):
        # todo: enable accept only for manual and FIFS
        if self.status != 0:
            raise ValidationError(detail=f"You can't accept {self.get_status_display()} application. ")
        self.status = 1
        self.save()
        if auto_join:
            self.join_group()
    
    def reject(self):
        if self.status != 0:
            raise ValidationError(detail=f"You can't accept {self.get_status_display()} application. ")
        self.status = 2
        self.save()
    
    def join_group(self):
        if self.status != 1:
            raise ValidationError(detail=f"Application to group not accepted, current status: {self.get_status_display()}. ")
        # if self.group_enrollment.limit_reached:
        #     raise ValidationError(detail="There are no empty spots in this group. ")
        # if not self.group_enrollment.can_join:
        #     raise ValidationError(detail="Decision deadline is over. ")
        existing_groups = CourseGroup.objects.filter(
            students=self.student,
            course__level=self.group_enrollment.course_group.course.level,
            course__subject=self.group_enrollment.course_group.course.subject
        )
        if existing_groups.exists():
            raise ValidationError(detail='Student is already in a group for the same level and subject. ')
        self.group_enrollment.add_student_to_group(self.student)
        self.joined = True
        self.save()
        return True
