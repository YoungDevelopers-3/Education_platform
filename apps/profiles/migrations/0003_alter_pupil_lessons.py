# Generated by Django 4.2.5 on 2023-10-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_lesson_times_timelesson_lesson_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupil',
            name='lessons',
            field=models.ManyToManyField(blank=True, null=True, related_name='pupils', to='profiles.lesson'),
        ),
    ]
