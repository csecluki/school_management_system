from users.management.commands.populate_database import PopulateCommand

from timetables.models import Period


class Command(PopulateCommand):
    help = 'Populate the timetables_period table with sample data. '
    
    def populate(self):
        config = self.config.get('period')
        Period.objects.all().delete()
        for year in range(config.get('start_year'), config.get('end_year')):
            Period.objects.create(start_date=f'{year - 1}-09-01', end_date=f'{year}-01-31')
            Period.objects.create(start_date=f'{year}-02-01', end_date=f'{year + 1}-06-30')
        self.stdout.write(self.style.SUCCESS(f'Successfully populated timetables_period. '))
