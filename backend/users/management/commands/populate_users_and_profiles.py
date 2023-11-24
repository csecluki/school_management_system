import random
from datetime import timezone

from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from faker import Faker
from django.core.management.base import BaseCommand
from users.models import User, Profile


fake = Faker()


class Command(BaseCommand):
    help = 'Populate users and profiles tables with random data.'

    STAFF_NUMBER = 2
    TEACHER_NUMBER = 15
    STUDENT_NUMBER = 500

    COUNTER = 0
    TOTAL_USERS = sum([STAFF_NUMBER, TEACHER_NUMBER, STUDENT_NUMBER])

    AGE = {
        'Teachers': {
            'minimum_age': 25,
            'maximum_age': 65
        },
        'Students': {
            'minimum_age': 18,
            'maximum_age': 26
        },
        'Staff': {
            'minimum_age': 30,
            'maximum_age': 60
        },
    }

    def handle(self, *args, **kwargs):
        self.populate_users_and_profiles()
        self.stdout.write(self.style.SUCCESS('Successfully populated users and profiles tables. '))

    def populate_users_and_profiles(self):
        User.objects.exclude(id=1).delete()
        Profile.objects.exclude(user_id=1).delete()
        self.populate_staff()
        self.populate_teachers()
        self.populate_students()

    def populate_staff(self):
        for _ in range(self.STAFF_NUMBER):
            user = User.objects.create_user(**self.get_user_data(f"staff{str(self.COUNTER).rjust(4, '0')}"))
            user.is_staff = True
            user.date_joined = fake.date_time_this_decade().astimezone(timezone.utc)
            user.save()

            self.update_profile(user, type_='Staff')

            self.COUNTER += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.COUNTER}/{self.TOTAL_USERS}) '))

    def populate_teachers(self):
        teacher_group = get_object_or_404(Group, name='Teachers')
        for _ in range(self.TEACHER_NUMBER):
            user = User.objects.create_user(**self.get_user_data(f"teacher{str(self.COUNTER).rjust(4, '0')}"))
            user.groups.add(teacher_group)
            user.date_joined = fake.date_time_this_decade().astimezone(timezone.utc)
            user.save()

            self.update_profile(user, type_='Teachers')

            self.COUNTER += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.COUNTER}/{self.TOTAL_USERS}) '))

    def populate_students(self):
        student_group = get_object_or_404(Group, name='Students')
        for _ in range(self.STUDENT_NUMBER):
            user = User.objects.create_user(**self.get_user_data(f"student{str(self.COUNTER).rjust(4, '0')}"))
            user.groups.add(student_group)
            user.date_joined = fake.date_time_this_decade().astimezone(timezone.utc)
            user.save()

            self.update_profile(user, type_='Students')

            self.COUNTER += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.COUNTER}/{self.TOTAL_USERS}) '))

    @staticmethod
    def get_user_data(username):
        return {
            'email': username + '@example.com',
            'password': 'securepassword'
        }

    def update_profile(self, user, type_):
        Profile.objects.update_or_create(
            user_id=user.id,
            defaults=self.get_profile_data(user, type_=type_)
        )

    def get_profile_data(self, user, type_):
        return {
            'user_id': user.id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'birth_date': fake.date_of_birth(**self.get_age_for_type(type_)),
            'bio': fake.text(max_nb_chars=random.randint(60, 300)),
        }

    def get_age_for_type(self, type_):
        return self.AGE.get(type_, {})
