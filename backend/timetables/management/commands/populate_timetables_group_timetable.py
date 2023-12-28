import random

from users.management.commands.populate_database import PopulateCommand
from rest_framework.exceptions import ValidationError
from timetables.models import GroupTimeTable, LessonUnit
from courses.models import CourseGroup


class Command(PopulateCommand):
    help = 'Populate the timetabes_group_timetable table with sample data'

    def populate(self):
        config = self.config.get('group_timetable', {})
        timetables_per_group = config.get("timetables_per_group", [])
        weights = config.get("weights", [])
        GroupTimeTable.objects.all().delete()
        
        lesson_units = LessonUnit.objects.all()

        for course_group in CourseGroup.objects.all():
            for _ in range(random.choices(timetables_per_group, weights)[0]):
                while True:
                    try:
                        GroupTimeTable.objects.create(
                            course_group=course_group,
                            day_of_week=random.choice(GroupTimeTable.WEEK_DAYS)[0],
                            lesson_unit=random.choice(lesson_units)
                        )
                    except ValidationError:
                        pass
                    else:
                        break

        self.stdout.write(self.style.SUCCESS((f'Successfully populated timetables_group_timetable. ')))
