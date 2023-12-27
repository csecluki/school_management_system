from abc import ABC
import json

from django.core.management.base import BaseCommand
from django.core.management import call_command


class PopulateCommand(ABC, BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument('--config', type=str, required=False, default='database_config.json',
                            help='Path to file with configuration. ')
    
    def load_config(self, path, part_name):
        with open(path) as file:
            return json.load(file).get(part_name)


class Command(PopulateCommand):
    help = 'Populate database. '

    def handle(self, *args, **options):
        config = options.get('config')
        call_command('populate_groups', config=config)
        call_command('populate_users_and_profiles', config=config)
        call_command('populate_rooms_room', config=config)
        call_command('populate_courses_subject', config=config)
        self.stdout.write(self.style.SUCCESS('Successfully populated database.'))
