from rest_framework.exceptions import ValidationError


def divisible_by_0_5(value):
    if value % 0.5 != 0:
        return value
    else:
        raise ValidationError(detail=f'Value {value} is not divisible by 0.5. ')


def not_1_5(value):
    if value != 1.5:
        return value
    else:
        raise ValidationError(detail=f"Note shouldn't be 1.5. ")
