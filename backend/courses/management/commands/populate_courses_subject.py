from users.management.commands.populate_database import PopulateCommand

from courses.models import Subject


class Command(PopulateCommand):
    help = 'Populate the courses_subject table with sample data. '
    
    def populate(self):
        config = self.config.get('subject', {})
        Subject.objects.all().delete()
        names = config.get('names')
        for i in range(min(config.get('number'), len(names))):
            Subject.objects.create(
                name=names[i]
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated courses_subject. '))
