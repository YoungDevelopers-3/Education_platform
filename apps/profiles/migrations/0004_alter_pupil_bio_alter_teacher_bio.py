# Generated by Django 4.2.5 on 2023-10-03 12:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_pupil_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupil',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
