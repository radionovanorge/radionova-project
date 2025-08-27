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
     q = request.GET.get('q', '').strip()
     selected_program = request.GET.get('program')
     selected_kategori = request.GET.get('kategori') 
     selected_tema = request.GET.get('tema')
     sort = request.GET.get('sort', 'Ny')

     posts = BlogPage.objects.live()

     # SMART SØKEFUNKSJONALITET
     if q:
         # Del opp søkeordet
         search_terms = q.split()

         # Først prøv eksakt søk
         exact_matches = posts.filter(title__iexact=q)

         # Deretter delvis matching i tittel (høy prioritet)
         title_matches = posts.filter(title__icontains=q)

         # Til slutt søk i alle felt
         all_field_query = Q()
         for term in search_terms:
             term_query = (
                 Q(title__icontains=term) |
                 Q(ingress__icontains=term) |
                 Q(search_description__icontains=term)
             )
             all_field_query |= term_query  # Bruk OR for mer fleksibilitet

         all_field_matches = posts.filter(all_field_query)

         # Kombiner og fjern duplikater
         posts = (exact_matches | title_matches | all_field_matches).distinct()

         # Manuell relevans-sortering
         def relevance_score(post):
             score = 0
             q_lower = q.lower()

             # Eksakt match i tittel = høyeste score
             if post.title.lower() == q_lower:
                 score += 100

             # Tittel starter med søkeord
             elif post.title.lower().startswith(q_lower):
                 score += 50

             # Søkeord i tittel
             elif q_lower in post.title.lower():
                 score += 25

             # Søkeord i ingress
             if post.ingress and q_lower in post.ingress.lower():
                 score += 10

             # Søkeord i beskrivelse
             if post.search_description and q_lower in post.search_description.lower():
                 score += 5

             return score

         # Sorter etter relevans
         posts = sorted(posts, key=relevance_score, reverse=True)

     else:
         posts = posts.order_by('-first_published_at')

     # FILTRERING (etter søk)
     if selected_program:
         if hasattr(posts, 'filter'):  # QuerySet
             posts = posts.filter(program__slug=selected_program)
         else:  # List (fra sorting)
             posts = [p for p in posts if p.program and p.program.slug == selected_program]

     if selected_kategori:
         if hasattr(posts, 'filter'):
             posts = posts.filter(typeArticle__iexact=selected_kategori)
         else:
             posts = [p for p in posts if p.typeArticle and p.typeArticle.lower() == selected_kategori.lower()]

     if selected_tema:
         if hasattr(posts, 'filter'):
             posts = posts.filter(program__category=selected_tema)
         else:
             posts = [p for p in posts if p.program and p.program.category == selected_tema]

     # Konverter tilbake til QuerySet hvis det er en liste
     if not hasattr(posts, 'filter') and posts:
         post_ids = [p.id for p in posts]
         posts = BlogPage.objects.filter(id__in=post_ids)
         # Bevar rekkefølgen
         preserved_order = {id: index for index, id in enumerate(post_ids)}
         posts = sorted(posts, key=lambda x: preserved_order[x.id])

     # SORTERING (kun hvis ikke søk)
     if not q and hasattr(posts, 'order_by'):
         if sort == 'Gammel':
             posts = posts.order_by('first_published_at')
         elif sort == 'asc':
             posts = posts.order_by('title')
         elif sort == 'desc':
             posts = posts.order_by('-title')

     # PAGINATION QUERYSTRING
     qs = request.GET.copy()
     if 'page' in qs:
         del qs['page']
     querystring = qs.urlencode()

     # Håndter count for lister vs QuerySet
     try:
         total_article_count = posts.count()  # QuerySet
     except (TypeError, AttributeError):
         total_article_count = len(posts)     # Liste

     paginator = Paginator(posts, 10)
     page_obj = paginator.get_page(request.GET.get("page"))

     return self.render(
         request,
         template='tears/nettsaker.html',
         context_overrides={
             "page_obj": page_obj,
             "all_posts": page_obj,
             "programs": ProgramPage.objects.live().order_by('title'),
             "categories": ProgramPage.CATEGORY_CHOICES,
             "q": q,
             "selected_program": selected_program,
             "selected_kategori": selected_kategori,
             "selected_tema": selected_tema,
             "sort": sort,
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
    ingress = models.CharField("Ingress", max_length=500, blank=True, help_text="Kort ingress/underoverskrift under tittelen")
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