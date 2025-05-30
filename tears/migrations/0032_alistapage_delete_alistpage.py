# Generated by Django 5.0.6 on 2025-02-17 15:45

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0031_remove_alistpage_alisteuke_remove_alistpage_tittel_and_more'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='AListaPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('uke', models.CharField(blank=True, help_text='Which week it is', max_length=255)),
                ('post_message', models.TextField(blank=True, help_text='Post message from Facebook')),
                ('images', wagtail.fields.StreamField([('image', 0)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {})})),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.DeleteModel(
            name='AListPage',
        ),
    ]
