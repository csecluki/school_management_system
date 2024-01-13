from django.core.exceptions import ValidationError


def step_5_min(value):
    if value.minute % 5 != 0:
        raise ValidationError('Please set the time with 5-minute intervals. ')


def full_minutes(value):
    if value.second != 0 or value.microsecond != 0:
        raise ValidationError('Please set the time with seconds and milliseconds set to 0. ')
