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
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from .blocks import Weekday, TimeChoices
from .blocks import ImageWithDescriptionBlock
from django.utils.timezone import now, localtime
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


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
    def all_posts(self):
        return BlogPage.objects.live().order_by('-last_published_at')
  

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_posts"] = BlogPage.objects.live(
        ).public().order_by("-date")[:9]
        context["latest_interviews"] = BlogPage.objects.live().filter(typeArticle="intervju").order_by('-first_published_at')[:4]
        context["latest_reviews"] = BlogPage.objects.live().filter(typeArticle="anmeldelse").order_by('-first_published_at')[:4]
        context["programs"] = ProgramPage.objects.live().order_by("?")
        context["dagtid_list"] = self.get_dagtid()
        context["latest_alister"] = AListaPage.objects.live().order_by("-first_published_at")[:3]
        context["latest_alista"] = self.get_latest_alista()
        context["all_posts"] = self.all_posts()
  
        return context
    
    """No need to routeablepages but we dont have model for nettsaker.html yet"""
    
    @route(r'^nettsaker/$', name='nettsaker')
    def nettsaker_page(self, request):
        selected_programs = request.GET.getlist('program')
        selected_tema     = request.GET.get('tema')
        selected_kategori = (request.GET.get('kategori') or '').lower()
    
        # Base querysets – allerede sortert etter først publisert
        blog_qs   = BlogPage.objects.live().order_by('-first_published_at')
        alista_qs = AListaPage.objects.live().order_by('-first_published_at')
    
        # Filtre som før
        if selected_programs:
            blog_qs   = blog_qs.filter(program__slug__in=selected_programs)
            alista_qs = alista_qs.filter(program__slug__in=selected_programs)
    
        if selected_tema:
            blog_qs   = blog_qs.filter(program__category=selected_tema)
            alista_qs = alista_qs.filter(program__category=selected_tema)
    
        if selected_kategori == 'a-lista':
            blog_qs   = BlogPage.objects.none()
        elif selected_kategori in {'article', 'anmeldelse', 'intervju'}:
            blog_qs   = blog_qs.filter(typeArticle=selected_kategori)
            alista_qs = AListaPage.objects.none()
        # ellers: begge typer er med
    
        # Normaliser til én liste med dato = first_published_at (ingen klokkeslett)
        items = []
    
        for p in blog_qs:
            d = p.first_published_at or p.latest_revision_created_at
            items.append({
                'title': p.title,
                'url': p.url,
                'date_obj': d,
                'date_iso': d.strftime('%Y-%m-%d') if d else '',
                'date_human': d.strftime('%d. %B %Y') if d else '',
                'ingress': p.ingress or p.search_description or '',
                'program_slug': p.program.slug if getattr(p, 'program', None) else '',
                'tema': p.program.category if getattr(p, 'program', None) and getattr(p.program, 'category', None) else '',
                'kategori': p.typeArticle.lower(),
                'kind': 'blog',
            })
    
        for a in alista_qs:
            d = a.first_published_at  # <-- kun first_published_at
            items.append({
                'title': a.title,
                'url': a.url,
                'date_obj': d,
                'date_iso': d.strftime('%Y-%m-%d') if d else '',
                'date_human': d.strftime('%d. %B %Y') if d else '',
                'ingress': a.ingress or '',
                'program_slug': a.program.slug if getattr(a, 'program', None) else '',
                'tema': a.program.category if getattr(a, 'program', None) and getattr(a.program, 'category', None) else '',
                'kategori': 'a-lista',
                'kind': 'a-lista',
            })
    
        # Sortér igjen i memory (belt & suspenders) – nyest først
        items.sort(key=lambda x: (x['date_obj'] or datetime.min), reverse=True)
    
        total_article_count = len(items)
    
        paginator = Paginator(items, 10)
        page_obj = paginator.get_page(request.GET.get("page"))
    
        qs = request.GET.copy(); qs.pop('page', None)
        querystring = qs.urlencode()
    
        return self.render(
            request,
            template='tears/nettsaker.html',
            context_overrides={
                "page_obj": page_obj,
                "all_posts": page_obj,
                "programs": ProgramPage.objects.live().order_by('title'),
                "categories": ProgramPage.CATEGORY_CHOICES,
                "selected_tema": selected_tema,
                "selected_programs": selected_programs,
                "selected_kategori": selected_kategori,
                "total_article_count": total_article_count,
                "querystring": querystring,
            }
        )
    
    
    
    
    
    
    
    
    
    

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

    sendetider = StreamField(
    [#we are using Choices in since timeblock does not support choices every half hour. Its in blocks.py 
        ("sendetid", blocks.StructBlock([
            ("weekday", blocks.ChoiceBlock(
                choices=Weekday.choices, required=False, help_text="Choose the day of the week")),
            ("start_time", blocks.ChoiceBlock(
                choices=TimeChoices.choices, required=False, help_text="Start time")),
            ("end_time", blocks.ChoiceBlock(
                choices=TimeChoices.choices, required=False, help_text="End time")),
        ])),
    ],
    blank=True,
    verbose_name="Sendetider (Broadcast Times)"
)
    

    #  Social Media Links
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
        FieldPanel("sendetider"),
        FieldPanel("instagram_link"),
        FieldPanel("facebook_link"),
        FieldPanel("tiktok_link"),
        FieldPanel("email_link"),
        FieldPanel("description"),
        
        
    ]
    
   
    


    


class BlogPage(Page): 
    page_description = "This is the blog page of the website and has the content at e.g. https://radionova.no/blog/2024/10/12/ny-blog."
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("Post time")
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    imageDecription = models.CharField("Bildetekst på hovedbilde:", max_length=255, blank=True, help_text="Bildetekst under første bildet")
    ingress = models.TextField("Ingress", max_length=500, blank=True, help_text="Kort ingress/underoverskrift under tittelen")
    overtittel = models.CharField("Navn på det du andmelder/intervjuer.", max_length=500, blank=True, help_text=" F.eks. '[Navn på festival]' eller '[Navn på artist]'.")
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
            ("image_with_description", ImageWithDescriptionBlock()),
            

            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
    )

    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("user"),
        FieldPanel("typeArticle"),
        FieldPanel("forfatter"),
        FieldPanel("ingress"),
        FieldPanel("overtittel"),
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("imageDecription"),
    ]
    def save(self, *args, **kwargs):
        # Auto-assign program based on parent page
        if not self.program:
            parent = self.get_parent()
            # Check if parent is a ProgramPage
            if parent and parent.__class__.__name__ == 'ProgramPage':
                self.program = parent
        super().save(*args, **kwargs)
    def related_posts(self):
        return BlogPage.objects.live().filter(program=self.program).exclude(id=self.id)[:3]
   
    


class FreeTextPage(Page):
    page_description = "These are pages with free text, can be used for additional pages like  /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
    def serve(self, request):
        # Get the latest child AListaPage
        latest_post = self.get_children().live().specific().order_by('-first_published_at').first()
        if latest_post:
            return HttpResponseRedirect(latest_post.url)
        return super().serve(request)  # fallback if no child pages exist
   

   

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
    

    

class AListaPage(Page): ##TODO: make it so only alista pages can be created under /a-lista/"
    page_description = "This page is for configuring A-lista for every week"
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    ingress = models.TextField(blank=True, help_text="ingress")
    dato = models.DateField("Dato", blank=True, null=True, help_text="Dato for A-lista")

    program = models.ForeignKey(
        'tears.ProgramPage',  
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='a_lista_posts',
        verbose_name="Redaksjon"
    )
    content = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("content", blocks.RichTextBlock()),
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("forfatter"),
        FieldPanel("program"),
        FieldPanel("ingress"),
        FieldPanel("dato"),
        FieldPanel("content"),
    ]
    def get_latest_alister(self, count=3):
        # Get sibling pages of type AListaPage (excluding self), ordered by date
        return AListaPage.objects.live().exclude(id=self.id).order_by('-first_published_at')[:count]

class Sendeplan(Page):
    page_description = "This page is for configuring sendeplan for the semester"

    def get_context(self, request):
        context = super().get_context(request)

        programs = ProgramPage.objects.live().all()
        sendeplan = {str(i): [] for i in range(1, 8)}  # 1=Mandag .. 7=Søndag

        current_time = localtime(now()).time()
        current_weekday = str(localtime(now()).isoweekday())

        for program in programs:
            for block in program.sendetider:
                data = block.value
                weekday = data.get("weekday")
                if weekday:
                    start_time_str = data.get("start_time")
                    end_time_str = data.get("end_time")

                    start_time = datetime.strptime(start_time_str, "%H:%M").time() if start_time_str else None
                    end_time = datetime.strptime(end_time_str, "%H:%M").time() if end_time_str else None

                    is_now = False
                    if weekday == current_weekday and start_time and end_time:
                        if start_time <= current_time <= end_time:
                            is_now = True
                    if start_time_str and end_time_str:
                        start_time_obj = datetime.strptime(start_time_str, "%H:%M")
                        end_time_obj = datetime.strptime(end_time_str, "%H:%M")
                        duration = (end_time_obj - start_time_obj).total_seconds() / 60  # minutes
                        rowspan = int(duration / 30)
                    else:
                     rowspan = 1  # default if missing times

                    sendeplan[weekday].append({
                        "title": program.title,
                        "start_time": start_time_str,
                        "end_time": end_time_str,
                        "category": program.get_category_display(),
                        "intro": program.intro,
                        "main_image": program.main_image,
                        "is_live_now": is_now,
                        "rowspan": rowspan,
                    })
                    
        context["sendeplan"] = sendeplan
        context["weekdays"] = ["1", "2", "3", "4", "5", "6", "7"]
        context["time_slots"] = ["00:00"] +[
            f"{hour:02d}:{minute:02d}" 
            for hour in range(6, 24) 
            for minute in (0, 30)
     ]  
         # Finner nåværende live program
        current_program = None

        for day_programs in sendeplan.values():
            for program in day_programs:
                if program["is_live_now"]:
                    current_program = program
                    break
            if current_program:
                break

        if current_program:
            context["current_live_text"] = f"Direkte: Radio Nova / {current_program['start_time']}–{current_program['end_time']}: {current_program['title']}"
        else:
            context["current_live_text"] = "Direkte: Radio Nova"       

        return context