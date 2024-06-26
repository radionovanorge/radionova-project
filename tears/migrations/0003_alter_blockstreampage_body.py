# Generated by Django 5.0.6 on 2024-05-31 21:09

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tears', '0002_alter_blockstreampage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockstreampage',
            name='body',
            field=wagtail.fields.StreamField([('full_width_banner', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.CharBlock()), ('background', wagtail.images.blocks.ImageChooserBlock()), ('gradient_color', wagtail.blocks.CharBlock(required=False)), ('buttons', wagtail.blocks.StreamBlock([('button', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('page', wagtail.blocks.PageChooserBlock(help_text='Link to a internal page (use eight this or the external url, not both.)', required=False)), ('external_url', wagtail.blocks.URLBlock(help_text='Link to an external url (use either this or the page, not both.)', required=False))]))], max_num=1, min_num=0, required=False))])), ('free_text', wagtail.blocks.StructBlock([('body', wagtail.blocks.RichTextBlock(required=False))]))], blank=True),
        ),
    ]
