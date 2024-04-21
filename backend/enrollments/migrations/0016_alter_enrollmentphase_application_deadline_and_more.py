# Generated by Django 4.2.7 on 2024-01-02 17:59

from django.db import migrations, models
import enrollments.validators


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0015_alter_groupenrollment_min_students'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentphase',
            name='application_deadline',
            field=models.DateTimeField(validators=[enrollments.validators.step_5_min, enrollments.validators.full_minutes]),
        ),
        migrations.AlterField(
            model_name='enrollmentphase',
            name='decision_deadline',
            field=models.DateTimeField(validators=[enrollments.validators.step_5_min, enrollments.validators.full_minutes]),
        ),
        migrations.AlterField(
            model_name='enrollmentphase',
            name='start_date',
            field=models.DateTimeField(validators=[enrollments.validators.step_5_min, enrollments.validators.full_minutes]),
        ),
        migrations.AlterField(
            model_name='groupenrollment',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'created'), (1, 'open'), (2, 'closed'), (3, 'cancelled')], default=0),
        ),
        migrations.AlterField(
            model_name='recruitmentstrategy',
            name='id',
            field=models.PositiveSmallIntegerField(choices=[(0, 'First in first served'), (1, 'Manual'), (2, 'Highest endgrade average')], primary_key=True, serialize=False),
        ),
    ]
