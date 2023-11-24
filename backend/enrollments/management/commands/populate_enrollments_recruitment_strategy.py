import random
from django.core.management.base import BaseCommand
from enrollments.models import RecruitmentStrategy


class Command(BaseCommand):
    help = 'Populate the enrollments_recruitment_strategy table with sample data'

    def handle(self, *args, **kwargs):

        data = [
            {'id': 0, 'is_auto_triggered': True},
            {'id': 1, 'is_auto_triggered': True},
        ]

        for item in data:
            rs, created = RecruitmentStrategy.objects.get_or_create(**item)
            if not created:
                self.stdout.write(self.style.SUCCESS(f'{rs.get_id_display()} strategy already existed. '))
            else:
                self.stdout.write(self.style.SUCCESS(f'{rs.get_id_display()} strategy created. '))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated enrollments_recruitment_strategy. '))
