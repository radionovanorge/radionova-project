# Generated by Django 5.0.6 on 2025-02-19 16:48

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0032_alistapage_delete_alistpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='dagtidpage',
            name='portrett_bilde',
            field=wagtail.fields.StreamField([('main_image', 0), ('content', 1)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {}), 1: ('wagtail.blocks.RichTextBlock', (), {})}),
        ),
    ]
