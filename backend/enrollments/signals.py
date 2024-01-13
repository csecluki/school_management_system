import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import GroupEnrollment, RecruitmentStrategy


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=GroupEnrollment)
def set_default_recruitment_strategy(sender, instance, **kwargs):
    if not instance.recruitment_strategy:
        instance.recruitment_strategy = RecruitmentStrategy.objects.get(id=0)
