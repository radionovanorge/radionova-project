# Generated by Django 5.2.1 on 2025-05-13 12:08

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0042_blogpage_imagedecription_alter_blogpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('main_image', 2), ('more_images', 3), ('content', 4)], blank=True, block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': True}), 1: ('wagtail.blocks.CharBlock', (), {'label': 'Bildebeskrivelse', 'max_length': 255, 'required': False}), 2: ('wagtail.blocks.StructBlock', [[('image', 0), ('description', 1)]], {}), 3: ('wagtail.blocks.ListBlock', (2,), {}), 4: ('wagtail.blocks.RichTextBlock', (), {})}),
        ),
    ]
