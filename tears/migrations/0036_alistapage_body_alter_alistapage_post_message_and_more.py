# Generated by Django 5.0.6 on 2025-04-01 13:37

import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0035_sendeplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='alistapage',
            name='body',
            field=wagtail.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='alistapage',
            name='post_message',
            field=models.TextField(blank=True, help_text='Underovskrift'),
        ),
        migrations.AlterField(
            model_name='alistapage',
            name='uke',
            field=models.CharField(blank=True, help_text='Hvilken uke er det?', max_length=255),
        ),
    ]
