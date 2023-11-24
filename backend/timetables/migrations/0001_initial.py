# Generated by Django 4.2.7 on 2023-11-24 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rooms', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonUnit',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
            options={
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CourseTimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday')])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('lesson_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scheduled_courses', to='timetables.lessonunit')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetables.period')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_room', to='rooms.room')),
            ],
            options={
                'default_permissions': (),
            },
        ),
    ]
