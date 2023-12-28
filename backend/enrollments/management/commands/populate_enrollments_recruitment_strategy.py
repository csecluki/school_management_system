from users.management.commands.populate_database import PopulateCommand
from enrollments.models import RecruitmentStrategy


class Command(PopulateCommand):
    help = 'Populate the enrollments_recruitment_strategy table with sample data'

    def populate(self):
        config = self.config.get('recruitment_strategy', {})
        data = config.get('data', {})

        for item in data:
            rs, created = RecruitmentStrategy.objects.get_or_create(**item)
            if not created:
                self.stdout.write(self.style.SUCCESS(f'{rs.get_id_display()} strategy already existed. '))
            else:
                self.stdout.write(self.style.SUCCESS(f'{rs.get_id_display()} strategy created. '))

        self.stdout.write(self.style.SUCCESS(f'Successfully populated enrollments_recruitment_strategy. '))
