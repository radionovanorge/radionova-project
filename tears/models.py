from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image



class HomePage( Page):
    page_description = "This is the homepage of the website and has the content at https://radionova.no. Don't edit this page unless you know what you are doing."
    
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
        ).public().order_by("-date")[:9]
        return context
  
    
    

class ProgrammerPage(Page):
    page_description = "This is the program list page of the website and has the content at https://radionova.no/programmer."
    subpage_types = ['ProgramPage']
    body  = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        return context
    

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
  


class ProgramPage(Page):
    page_description = "This is the program page of the website and has the content at e.g. https://radionova.no/programmer/frokost."
    subpage_types = ['BlogPage']
    CATEGORY_CHOICES = [
        ("aktualitet", "Aktualitet"),
        ("humor_underholdning", "Humor & underholdning"),
        ("kultur", "Kultur"),
        ("musikk", "Musikk"),
        ("tema", "Tema"),
        ("tidligere_programmer", "Tidligere programmer"),
    ]
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="aktualitet"
    )
    program = models.ForeignKey(Group, on_delete=models.PROTECT) 

    intro = models.CharField("Introduksjon", max_length=255, blank=True) 


    description = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("program"),
        FieldPanel("intro"),
        FieldPanel("description"),
        
    ]

    


class BlogPage(Page):
    page_description = "This is the blog page of the website and has the content at e.g. https://radionova.no/blog/2024/10/12/ny-blog."
    redaksjon = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("Post time")
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    imageDecription = models.CharField("BildeTekst:", max_length=255, blank=True)
    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("redaksjon"),
        FieldPanel("forfatter"),
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("imageDecription")
    ]
  


class FreeTextPage(Page):
    page_description = "These are pages with free text, can be used for additional pages like  /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
   

   

class DagTidPage(Page):
    page_description = "This are page is for configuring Dagtid names, roles etc."

    
    DagTidNavn = models.CharField("DagTidNavn", max_length=255, blank=True)
    Rolle = models.CharField("Rolle:", max_length=255, blank=True)
    beskrivelse = models.CharField("beskrivelse:", max_length=255, blank=True)

    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("DagTidNavn"),
        FieldPanel("Rolle"),
        FieldPanel("beskrivelse"),
    ]

    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    

class AListPage(Page):
    page_description = "This are page is for configuring a-lista for every week"

    
    AListeUke = models.CharField("AListeUke", max_length=255, blank=True)
    date = models.DateTimeField("Post time")
    Tittel = models.CharField("Tittel:", max_length=255, blank=True)

    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("AListeUke"),
        FieldPanel("date"),
        FieldPanel("Tittel"),
        FieldPanel("body"),
    ]

    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

  



