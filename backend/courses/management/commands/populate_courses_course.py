from django.core.management.base import BaseCommand
from django.db import IntegrityError
from courses.models import Course, Subject
from users.models import User

import random
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Populate the Course model with sample data'

    MAX_COURSES_PER_TEACHER = 10

    def handle(self, *args, **options):
        Course.objects.all().delete()
        teachers = User.objects.filter(groups__name='Teachers')
        subjects = Subject.objects.all()

        for teacher in teachers:
            for _ in range(int(random.triangular(2, 10, 7))):
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
