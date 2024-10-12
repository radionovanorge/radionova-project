from django.db import models
from django.contrib.auth.models import User, Group
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    page_description = "This is the homepage of the website "
    "and has the content at https://radionova.no. Don't edit this page unless you know what you are doing."
    
    content = StreamField(
        [
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Home Page"

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_posts"] = BlogPage.objects.live(
        ).public().order_by("-date")[:5]
        return context


class ProgramPage(Page):
    page_description = "This is the program page of the website "
    "and has the content at e.g. https://radionova.no/programmer/studentnyhetene."
    subpage_types = ['BlogPage']
    program = models.ForeignKey(Group, on_delete=models.PROTECT)
    description = StreamField(
        [
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("program"),
        FieldPanel("description"),
    ]


class BlogPage(Page):
    page_description = "This is the blog page of the website "
    "and has the content at e.g. https://radionova.no/blog/2024/10/12/ny-blog."
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("Post time")
    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("date"),
        FieldPanel("body"),
    ]


class FreeTextPage(Page):
    page_description = "These are pages with free text, can be used for additional pages like "
    "/om-oss, /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
