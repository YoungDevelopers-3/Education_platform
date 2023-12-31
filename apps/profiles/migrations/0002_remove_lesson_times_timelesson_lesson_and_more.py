# Generated by Django 4.2.5 on 2023-09-29 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='times',
        ),
        migrations.AddField(
            model_name='timelesson',
            name='lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='times', to='profiles.lesson'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='timelesson',
            name='day',
            field=models.CharField(choices=[('dushanba', 'dushanba'), ('seshanba', 'seshanba'), ('chorshanba', 'payshanba'), ('payshanba', 'payshanba'), ('juma', 'juma'), ('shanba', 'shanba'), ('yakshanba', 'yakshanba')], max_length=15),
        ),
    ]
