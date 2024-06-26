from django.contrib.auth.models import Group, Permission
from users.management.commands.populate_database import PopulateCommand


class Command(PopulateCommand):
    help = 'Create predefined groups in the database and assign permissions to them. '
    
    def populate(self):
        for name, permissions in self.config.items():
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{name}" created successfully. '))
            else:
                self.stdout.write(self.style.SUCCESS(f'Group "{name}" already exists. '))

            for permission_code in permissions:
                app_label, codename = permission_code.split('.')
                permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                if not group.permissions.filter(id=permission.id).exists():
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Permission "{permission}" added to group "{name}". '))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Permission "{permission}" already assigned to group "{name}". '))
        self.stdout.write(self.style.SUCCESS('Groups and permissions created successfully.'))
