# Generated by Django 4.2.5 on 2023-10-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_role_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('code', 'code'), ('done', 'done')], default='new'),
        ),
    ]
