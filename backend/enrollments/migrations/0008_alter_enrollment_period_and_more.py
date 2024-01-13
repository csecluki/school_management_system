# Generated by Django 4.2.7 on 2023-12-31 12:05

from django.db import migrations, models
import django.db.models.deletion
import timetables.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0001_initial'),
        ('enrollments', '0007_alter_enrollment_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='period',
            field=models.ForeignKey(default=timetables.models.PeriodManager.get_next_period, on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='timetables.period'),
        ),
        migrations.AlterField(
            model_name='enrollmentphase',
            name='enrollment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='phases', to='enrollments.enrollment'),
        ),
    ]
