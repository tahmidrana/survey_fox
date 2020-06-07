# Generated by Django 3.0.6 on 2020-06-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20200602_2318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionnaire',
            name='finish_at',
        ),
        migrations.RemoveField(
            model_name='questionnaire',
            name='starting_at',
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='is_started',
            field=models.BooleanField(default=False),
        ),
    ]
