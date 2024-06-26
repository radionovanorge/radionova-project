# Generated by Django 5.0.6 on 2024-06-02 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0008_alter_blogpage_author'),
        ('wagtailcore', '0093_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'verbose_name': 'Home Page',
            },
            bases=('wagtailcore.page',),
        ),
    ]
