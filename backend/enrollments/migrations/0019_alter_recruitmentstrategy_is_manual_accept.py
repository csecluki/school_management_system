# Generated by Django 4.2.7 on 2024-01-06 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0018_recruitmentstrategy_is_manual_accept_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruitmentstrategy',
            name='is_manual_accept',
            field=models.BooleanField(),
        ),
    ]
