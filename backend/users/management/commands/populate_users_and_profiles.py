import random

from datetime import timezone
from faker import Faker

from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import get_object_or_404
from users.management.commands.populate_database import PopulateCommand
from users.models import User, Profile


fake = Faker()


class Command(PopulateCommand):
    help = 'Populate users and profiles tables with random data.'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.counter = 0

    def populate(self):
        self.total_users = self.get_total_user_number()
        User.objects.exclude(is_superuser=True).delete()
        Profile.objects.exclude(user__is_superuser=True).delete()
        self.populate_staff()
        self.populate_teachers()
        self.populate_students()
        self.stdout.write(self.style.SUCCESS('Successfully populated users and profiles tables. '))
    
    def get_total_user_number(self):
        return self.config.get('staff_number', 0) + self.config.get('teacher_number', 0) + self.config.get('student_number', 0)

    def populate_staff(self):
        for _ in range(self.config.get('staff_number')):
            user = User.objects.create_user(**self.get_user_data(f"staff{self.get_user_number()}"))
            user.is_staff = True

            self.save_user(user)
            self.update_profile(user, type_='Staff')

            self.counter += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.counter}/{self.total_users}) '))

    def populate_teachers(self):
        teacher_group = get_object_or_404(Group, name='Teachers')
        for _ in range(self.config.get('teacher_number')):
            user = User.objects.create_user(**self.get_user_data(f"teacher{self.get_user_number()}"))
            user.groups.add(teacher_group)

            self.save_user(user)
            self.update_profile(user, type_='Teachers')

            self.counter += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.counter}/{self.total_users}) '))

    def populate_students(self):
        student_group = get_object_or_404(Group, name='Students')
        for _ in range(self.config.get('student_number')):
            user = User.objects.create_user(**self.get_user_data(f"student{self.get_user_number()}"))
            user.groups.add(student_group)

            self.save_user(user)
            self.update_profile(user, type_='Students')

            self.counter += 1
            self.stdout.write(self.style.SUCCESS(f'Successfully created user and profile for {user} ({self.counter}/{self.total_users}) '))

    @staticmethod
    def get_user_data(username):
        return {
            'email': username + '@example.com',
            'password': 'securepassword'
        }
    
    def get_user_number(self):
        return str(self.counter).rjust(4, '0')
    
    def save_user(self, user):        
        user.date_joined = fake.date_time_this_decade().astimezone(timezone.utc)
        user.save()

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
        return self.config.get('age', {}).get(type_, {})
