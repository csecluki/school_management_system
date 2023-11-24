from django.core.management.base import BaseCommand
from courses.models import Course, Subject
from users.models import User

import random
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    help = 'Populate the Course model with sample data'

    MAX_COURSES_PER_TEACHER = 10
    TOTAL_COURSES = 100


    def handle(self, *args, **options):
        Course.objects.all().delete()

        teachers = User.objects.filter(groups__name='Teachers')
        subjects = Subject.objects.all()

        for _ in range(self.TOTAL_COURSES):
            Course.objects.create(
                subject=random.choice(subjects),
                level=random.choice(Course.LEVEL_CHOICES)[0],
                teacher=self.get_teacher(teachers),
                description=faker.text(random.randint(60, 300)),
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated courses_course. '))
    
    def get_teacher(self, teachers):
        while True:
            teacher = random.choice(teachers)
            if not Course.objects.filter(teacher=teacher).count() >= self.MAX_COURSES_PER_TEACHER:
                return teacher
