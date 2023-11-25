from django.core.management.base import BaseCommand
from timetables.models import Period


class Command(BaseCommand):
    help = 'Populate the timetables_period table with sample data'

    def handle(self, *args, **kwargs):
        Period.objects.all().delete()

        for year in range(2023, 2026):
            Period.objects.create(start_date=f'{year - 1}-09-01', end_date=f'{year}-01-31')
            Period.objects.create(start_date=f'{year}-02-01', end_date=f'{year + 1}-06-30')

        self.stdout.write(self.style.SUCCESS(f'Successfully created Period instances. '))
