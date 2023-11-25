
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import GroupEnrollment, RecruitmentStrategy


@receiver(pre_save, sender=GroupEnrollment)
def set_default_recruitment_strategy(sender, instance, **kwargs):
    if not instance.recruitment_strategy:
        default_strategy, _ = RecruitmentStrategy.objects.get(id=0)
        instance.recruitment_strategy = default_strategy
