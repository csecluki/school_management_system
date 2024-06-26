# Generated by Django 4.2.7 on 2023-12-27 11:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_alter_coursegroup_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursegroup',
            name='students',
            field=models.ManyToManyField(related_name='enrolled_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
