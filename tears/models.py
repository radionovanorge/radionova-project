from django.db import models
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

class HomePage(RoutablePageMixin, Page):
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
    
    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        return self.render(request, template='tears/nettsaker.html')
    
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')
    
    @route(r'^alista/$', name='alista') 
    def alista_page(self, request):
        return self.render(request, template='tears/alista.html')

  
    
    
        
    



class ProgrammerPage(Page, RoutablePageMixin):
    page_description = "This is the program list page of the website and has the content at https://radionova.no/programmer."
    subpage_types = ['ProgramPage']
    body  = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        return context
    

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')

    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        return self.render(request, template='tears/nettsaker.html')
    
    @route(r'^alista/$', name='alista') 
    def alista_page(self, request):
        return self.render(request, template='tears/alista.html')



class ProgramPage(Page , RoutablePageMixin):
    page_description = "This is the program page of the website and has the content at e.g. https://radionova.no/programmer/frokost."
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
  


class BlogPage(Page, RoutablePageMixin):
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
    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        self.render(request, template='tears/nettsaker.html')
    
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')
    
    @route(r'^alista/$', name='alista') 
    def alista_page(self, request):
        return self.render(request, template='tears/alista.html')


class FreeTextPage(Page, RoutablePageMixin):
    page_description = "These are pages with free text, can be used for additional pages like  /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        self.render(request, template='tears/nettsaker.html')
    
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')
    @route(r'^alista/$', name='alista') 
    def alista_page(self, request):
        return self.render(request, template='tears/alista.html')

class DagTidPage(Page, RoutablePageMixin):
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

    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        self.render(request, template='tears/nettsaker.html')
    
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')
    @route(r'^alista/$', name='alista') 
    def alista_page(self, request):
        return self.render(request, template='tears/alista.html')
    


class AListPage(Page, RoutablePageMixin):
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

    @route(r'^$', name='home') 
    def home_page(self, request):
        return self.render(request, template='tears/home_page.html')

    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        self.render(request, template='tears/nettsaker.html')
    
    @route(r'^programmer/$', name='programmer') 
    def programmer_page(self, request):
        return self.render(request, template='tears/programmer_page.html')
    





