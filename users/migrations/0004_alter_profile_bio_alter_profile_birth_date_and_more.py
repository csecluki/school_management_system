# Generated by Django 4.1.3 on 2022-11-05 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='second_name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
