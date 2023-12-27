from django.db import transaction
from users.management.commands.populate_database import PopulateCommand

from courses.models import Subject


class Command(PopulateCommand):
    help = 'Populate the courses_subject table with sample data'

    def handle(self, *args, **options):
        self.config = self.load_config(options.get('config'), 'courses')
        with transaction.atomic():
            self.populate_rooms()
    
    def populate_rooms(self):
        config = self.config.get('subjects', {})
        names = config.get('names')
        for i in range(min(config.get('number'), len(names))):
            Subject.objects.get_or_create(
                name=names[i]
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated courses_subject. '))
