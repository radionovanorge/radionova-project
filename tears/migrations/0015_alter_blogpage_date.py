# Generated by Django 5.0.6 on 2024-06-04 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0014_rename_organizers_program_hosts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateTimeField(verbose_name='Post time'),
        ),
    ]