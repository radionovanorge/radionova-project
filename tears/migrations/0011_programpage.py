# Generated by Django 5.0.6 on 2024-06-03 12:18

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0010_program_broadcastschedule'),
        ('wagtailcore', '0093_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('description', wagtail.fields.RichTextField(blank=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tears.program')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
