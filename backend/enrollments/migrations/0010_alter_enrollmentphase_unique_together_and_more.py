# Generated by Django 4.2.7 on 2023-12-31 19:28

from django.db import migrations, models
import django.db.models.deletion
import timetables.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0001_initial'),
        ('enrollments', '0009_alter_enrollment_period_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enrollmentphase',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='period',
            field=models.ForeignKey(default=timetables.models.PeriodManager.get_next_period, on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='timetables.period'),
        ),
    ]