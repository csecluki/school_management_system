from abc import ABC, abstractmethod
import json

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from timetables.models import Period


class PopulateCommand(ABC, BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument('--config', type=str, required=False, default='database_config.json',
                            help='Path to file with configuration. ')
        parser.add_argument('--config_part', type=str, required=False, default='',
                            help='Section name from config. ')
        parser.add_argument('--period', type=str, required=False, default='',
                            help='''Period id for which data should be inserted.
                            If "" - first period will be selected. ''')

    def handle(self, *args, **options):
        self.config = self.load_config(options.get('config'), options.get('config_part'))
        with transaction.atomic():
            self.populate()
    
    def load_config(self, path, part_name):
        with open(path) as file:
            return json.load(file).get(part_name)
    
    @abstractmethod
    def populate(self):
        pass
    
    @staticmethod
    def get_period(period_id):
        try:
            return get_object_or_404(Period, id=period_id)
        except Http404:
            return Period.objects.order_by('id').first()


class Command(PopulateCommand):
    help = 'Populate database. '

    def handle(self, *args, **options):
        config = options.get('config')
        call_command('populate_groups', config=config, config_part='groups')
        call_command('populate_users_and_profiles', config=config, config_part='users')
        call_command('populate_rooms_room', config=config, config_part='rooms')
        call_command('populate_courses_subject', config=config, config_part='courses')
        call_command('populate_timetables_period', config=config, config_part='timetables')
        call_command('populate_timetables_lesson_unit', config=config, config_part='timetables')
        call_command('populate_courses_course', config=config, config_part='courses')
        call_command('populate_courses_course_group', config=config, config_part='courses')
        call_command('populate_timetables_group_timetable', config=config, config_part='timetables')
        call_command('populate_enrollments_recruitment_strategy', config=config, config_part='enrollments')
        call_command('populate_enrollments_group_enrollment', config=config, config_part='enrollments')
        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))
    
    def populate(self):
        return super().populate()
