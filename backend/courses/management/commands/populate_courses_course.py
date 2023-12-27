from users.management.commands.populate_database import PopulateCommand
from django.db import IntegrityError
from courses.models import Course, Subject
from users.models import User

import random
from faker import Faker

faker = Faker()


class Command(PopulateCommand):
    help = 'Populate the Course model with sample data'

    def populate(self):
        config = self.config.get('course')
        Course.objects.all().delete()
        teachers = User.objects.filter(groups__name='Teachers')
        subjects = Subject.objects.all()

        for teacher in teachers:
            for _ in range(self.get_course_range(config)):
                while True:
                    try:
                        Course.objects.create(
                            subject=random.choice(subjects),
                            level=random.choice(Course.LEVEL_CHOICES)[0],
                            teacher=teacher,
                            description=faker.text(random.randint(60, 250)),
                        )
                    except IntegrityError:
                        pass
                    else:
                        break

        self.stdout.write(self.style.SUCCESS('Successfully populated courses_course. '))
    
    @staticmethod
    def get_course_range(config):
        return int(
            random.triangular(
                config.get('max_courses_per_teacher'),
                config.get('max_courses_per_teacher'),
                config.get('mode_courses_per_teacher')
            )
        )
