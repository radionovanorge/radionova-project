from django.db import models
from wagtail.embeds.oembed_providers import youtube, vimeo, spotify

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import MultipleChooserPanel


class BlogIndexPage(Page):
    is_creatable = False
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class BlogPage(Page):
    date = models.DateField("Post date")
    headline = models.CharField(max_length=255)
    facts = RichTextField(features=["ul"], blank=True)
    body = RichTextField(blank=True)

    subpage_types = []

    search_fields = Page.search_fields + [
        index.SearchField("headline"),
        index.SearchField("body"),
        index.SearchField("facts"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("headline"),
        FieldPanel("facts"),
        FieldPanel("body", classname="full"),
        InlinePanel("gallery_images", label="Gallery images"),
        MultipleChooserPanel(
            "gallery_images", label="Gallery images", chooser_field_name="image"
        ),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]
