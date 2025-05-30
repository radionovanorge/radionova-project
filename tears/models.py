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

    def get_latest_alista(self):
        return AListaPage.objects.live().order_by('-first_published_at').first()
    
    def get_dagtid(self):
        """Fetch all Dagtid members"""
        return DagTidPage.objects.live().order_by('-first_published_at')

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_posts"] = BlogPage.objects.live(
        ).public().order_by("-date")[:9]
        context["latest_interviews"] = BlogPage.objects.live().filter(typeArticle="intervju").order_by('-first_published_at')[:4]
        context["latest_reviews"] = BlogPage.objects.live().filter(typeArticle="anmeldelse").order_by('-first_published_at')[:4]
        context["programs"] = ProgramPage.objects.live().order_by("?")
        context["dagtid_list"] = self.get_dagtid()
        return context
    
    """No need to routeablepages but we dont have model for nettsaker.html yet"""
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        return self.render(request, template='tears/nettsaker.html')
    

    


    
    

class ProgrammerPage(Page):
    page_description = "This is the program list page of the website and has the content at https://radionova.no/programmer."
    subpage_types = ['ProgramPage']
    body  = RichTextField(blank=True)

  

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]
    subpage_types = ['ProgramPage']

    def get_context(self, request):
        context = super().get_context(request)

        # Predefined categories to group by
        categories = [
            ("Aktualitet", "aktualitet"),
            ("Humor & underholdning", "humor_underholdning"),
            ("Kultur", "kultur"),
            ("Musikk", "musikk"),
            ("Tema", "tema"),
            ("Tidligere programmer", "tidligere_programmer"),
        ]

        # Group programs by category
        grouped_programs = {
            display_name: ProgramPage.objects.live().filter(category=category)
            for display_name, category in categories
        }
        total_program_count = sum(len(programs) for programs in grouped_programs.values())
        context["grouped_programs"] = grouped_programs
        context["total_program_count"] = total_program_count 
        
        return context
  


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

    program = models.ForeignKey(
        Group,
        on_delete=models.PROTECT
    )

    main_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hovedbilde",
    )

    intro = models.CharField("Introduksjon", max_length=255, blank=True)

    # 🕒 New field: Day and Time string
    schedule_info = models.CharField("Sendetid", max_length=100, blank=True, help_text="F.eks: Mandager · 19:00 - 20:30")

    # 🔗 Social Media Links
    instagram_link = models.URLField("Instagram-link", blank=True)
    facebook_link = models.URLField("Facebook-link", blank=True)
    tiktok_link = models.URLField("TikTok-link", blank=True)
    email_link = models.URLField("E-post-link", blank=True)

    description = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("program"),
        FieldPanel("main_image"),
        FieldPanel("intro"),
        FieldPanel("schedule_info"),
        FieldPanel("instagram_link"),
        FieldPanel("facebook_link"),
        FieldPanel("tiktok_link"),
        FieldPanel("email_link"),
        FieldPanel("description"),
    ]
    


    


class BlogPage(Page): #TODO add an article|anmeldelse|intervju field
    page_description = "This is the blog page of the website and has the content at e.g. https://radionova.no/blog/2024/10/12/ny-blog."
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("Post time")
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    imageDecription = models.CharField("BildeTekst:", max_length=255, blank=True, help_text="BildeTekst under første bildet")
    ingress = models.CharField("Ingress", max_length=500, blank=True, help_text="Kort ingress/underoverskrift under tittelen")
    overtittel = models.CharField("Overtittel", max_length=500, blank=True, help_text="Kort overtittel under hovedtittelen. For intervju er dette navnet på den som er intervjuet, for anmeldelse er det hva du anmelder (enten det er Film, Spisested eller Musikk), for vanlig nettsak trengs det ikke å skrive noe")
    #this is for having nettsaker in programpages. makes it possible to show programs each nettsak they have made only

    program = models.ForeignKey(
        'tears.ProgramPage',  
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='blog_posts',
        verbose_name="Redaksjon"
    )
    typeArticle = models.CharField(
        max_length=50,
        choices=[
            ("article", "Artikkel"),
            ("anmeldelse", "Anmeldelse"),
            ("intervju", "Intervju"),
        ],
        default="article",
        verbose_name="Type of Article"
    )
    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("imageDecription", blocks.CharBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("user"),
        FieldPanel("typeArticle"),
        FieldPanel("program"),
        FieldPanel("forfatter"),
        FieldPanel("ingress"),
        FieldPanel("overtittel"),
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("imageDecription"),
    ]
    def related_posts(self):
        return BlogPage.objects.live().filter(program=self.program).exclude(id=self.id)[:3]
  


class FreeTextPage(Page):
    page_description = "These are pages with free text, can be used for additional pages like  /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
   

   

class DagTidPage(Page):
    page_description = "This page is for configuring DagTid, About Radio Nova, and Omtaler i medier."

    # Free text for 'About Radio Nova' (top part)
    about_radio_nova = StreamField(
        [
            ("content", blocks.RichTextBlock()),
            ("main_image", ImageChooserBlock()),
        ],
        blank=True,
        verbose_name="About Radio Nova"
    )

    # Repeating Employees
    ansatte = StreamField(
        [
            ("ansatt", blocks.StructBlock([
                ("name", blocks.CharBlock(required=True, help_text="Employee full name")),
                ("role", blocks.CharBlock(required=True, help_text="Their role/title")),
                ("email", blocks.CharBlock(required=False, help_text="Their email address")),
                ("image", ImageChooserBlock(required=False)),
            ])),
        ],
        blank=True,
        verbose_name="Ansatte (Employees)"
    )

    # Repeating Media Mentions
    omtaler_i_medier = StreamField(
        [
            ("omtale", blocks.StructBlock([
                ("title", blocks.CharBlock(required=True)),
                ("date", blocks.DateBlock(required=True)),
                ("description", blocks.TextBlock(required=True)),
                ("link", blocks.URLBlock(required=True)),
                ("image", ImageChooserBlock(required=True)),
            ])),
        ],
        blank=True,
        verbose_name="Omtaler i andre medier"
    )

    content_panels = Page.content_panels + [
    FieldPanel("about_radio_nova"),
    FieldPanel("ansatte"),
    FieldPanel("omtaler_i_medier"),
]

    subpage_types = []
    

    

class AListaPage(Page):
    page_description = "This page is for configuring A-lista for every week"
    body = RichTextField(blank=True)
    uke = models.CharField(max_length=255, blank=True, help_text="Hvilken uke er det?")
    post_message = models.TextField(blank=True, help_text="Underovskrift")

    images = StreamField([
        ("image", ImageChooserBlock()),  # Allows multiple image uploads
    ], blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("uke"),
        FieldPanel("post_message"),
        FieldPanel("images"),
        FieldPanel("body"),
    ]

class Sendeplan(Page):
     page_description = "This page is for configuring sendeplan for the semester"
    
    #def get_context(self, request):
     #   context = super().get_context(request)
      #  return context
      # context["programs"] = sendplan.objects.live().order_by("?")
      #  return context




