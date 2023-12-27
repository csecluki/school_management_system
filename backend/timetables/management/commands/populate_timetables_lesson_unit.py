from users.management.commands.populate_database import PopulateCommand
from timetables.models import LessonUnit


class Command(PopulateCommand):
    help = 'Populate the timetables_lesson_unit table with sample data'

    def populate(self):
        data = self.config.get('lesson_unit')
        LessonUnit.objects.all().delete()
        for unit in data:
            LessonUnit.objects.create(**unit)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated timetables_lesson_unit. '))
