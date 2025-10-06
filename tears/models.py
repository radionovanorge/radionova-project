from django.db import models
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

from django import forms
from django.contrib.auth import get_user_model
from .blocks import CenteredFlexBlock
from wagtail.admin.forms import WagtailAdminPageForm



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
        return AListaPage.objects.live().order_by("-first_published_at").first()

    def get_dagtid(self):
        """Fetch all Dagtid members"""
        return DagTidPage.objects.live().order_by("-first_published_at")

    def all_posts(self):
        return BlogPage.objects.live().order_by("-last_published_at")

    def get_context(self, request):
        context = super().get_context(request)
        context["latest_posts"] = BlogPage.objects.live().public().order_by("-date")[:9]
        context["latest_interviews"] = (
            BlogPage.objects.live()
            .filter(typeArticle="intervju")
            .order_by("-first_published_at")[:4]
        )
        context["latest_reviews"] = (
            BlogPage.objects.live()
            .filter(typeArticle="anmeldelse")
            .order_by("-first_published_at")[:4]
        )
        context["programs"] = ProgramPage.objects.live().order_by("?")
        context["dagtid_list"] = self.get_dagtid()
        context["latest_alister"] = AListaPage.objects.live().order_by(
            "-first_published_at"
        )[:3]
        context["latest_alista"] = self.get_latest_alista()
        context["all_posts"] = self.all_posts()

        return context

    """No need to routeablepages but we dont have model for nettsaker.html yet"""

    @route(r"^nettsaker/$", name="nettsaker")
    def nettsaker_page(self, request):
        selected_programs = [p for p in request.GET.getlist("program") if p.strip()]
        selected_tema = request.GET.get("tema", "").strip() or None
        selected_kategori = (request.GET.get("kategori", "").strip() or "").lower()
        search_query = request.GET.get("q", "").strip()  # Get search query
        sort_order = request.GET.get("sort", "Ny")  # Get sort parameter

        # Base querysets
        blog_qs = BlogPage.objects.live()
        alista_qs = AListaPage.objects.live()

        # Apply filters FIRST (before search, since search returns PostgresSearchResults)
        if selected_programs:
            blog_qs = blog_qs.filter(program__slug__in=selected_programs)
            alista_qs = alista_qs.filter(program__slug__in=selected_programs)

        if selected_tema:
            blog_qs = blog_qs.filter(program__category=selected_tema)
            alista_qs = alista_qs.filter(program__category=selected_tema)

        if selected_kategori == "a-lista":
            blog_qs = BlogPage.objects.none()
        elif selected_kategori in {"article", "anmeldelse", "intervju"}:
            blog_qs = blog_qs.filter(typeArticle=selected_kategori)
            alista_qs = AListaPage.objects.none()

        # Apply search filter AFTER other filters
        if search_query:
            blog_qs = blog_qs.filter(
                Q(title__icontains=search_query)
                | Q(ingress__icontains=search_query)
                | Q(forfatter__icontains=search_query)  # <-- author text field
                | Q(
                    user__first_name__icontains=search_query
                )  # <-- optional: Django User
                | Q(user__last_name__icontains=search_query)
                | Q(search_description__icontains=search_query)
            )
            alista_qs = alista_qs.filter(
                Q(title__icontains=search_query) | Q(ingress__icontains=search_query)
            )

        # Convert to list with proper date handling
        items = []

        for p in blog_qs:
            d = p.first_published_at or p.latest_revision_created_at
            #main_img to nettsaker
            main_img = None
            if p.body:
                for block in p.body:
                    if block.block_type == "main_image":
                        main_img = block.value
                        break 
           
            items.append(
                {
                    "title": p.title,
                    "url": p.url,
                    "date_obj": d,
                    "date_iso": d.strftime("%Y-%m-%d") if d else "",
                    "date_human": d.strftime("%d. %B %Y") if d else "",
                    "ingress": p.ingress or p.search_description or "",
                    "program_slug": p.program.slug
                    if getattr(p, "program", None)
                    else "",
                    "tema": p.program.category
                    if getattr(p, "program", None)
                    and getattr(p.program, "category", None)
                    else "",
                    "kategori": p.typeArticle.lower(),
                    "kind": "blog",
                    "image": main_img,
                }
            )

        for a in alista_qs:
            d = a.first_published_at
            #main_img to nettasker
            main_img = None
            if a.content:
             for block in a.content:
                 if block.block_type == "main_image":
                     main_img = block.value
                     break
            
            items.append(
                {
                    "title": a.title,
                    "url": a.url,
                    "date_obj": d,
                    "date_iso": d.strftime("%Y-%m-%d") if d else "",
                    "date_human": d.strftime("%d. %B %Y") if d else "",
                    "ingress": a.ingress or "",
                    "program_slug": a.program.slug
                    if getattr(a, "program", None)
                    else "",
                    "tema": a.program.category
                    if getattr(a, "program", None)
                    and getattr(a.program, "category", None)
                    else "",
                    "kategori": "a-lista",
                    "kind": "a-lista",
                    "image": main_img,
                }
            )

        # Apply sorting
        if sort_order == "Gammel":  # Oldest first
            items.sort(key=lambda x: (x["date_obj"] or datetime.min), reverse=False)
        elif sort_order == "asc":  # A-Å
            items.sort(key=lambda x: x["title"].lower())
        elif sort_order == "desc":  # Å-A
            items.sort(key=lambda x: x["title"].lower(), reverse=True)
        else:  # Default: Newest first
            items.sort(key=lambda x: (x["date_obj"] or datetime.min), reverse=True)

        total_article_count = len(items)

        paginator = Paginator(items, 10)
        page_obj = paginator.get_page(request.GET.get("page"))

        # Preserve all parameters for pagination
        qs = request.GET.copy()
        qs.pop("page", None)
        querystring = qs.urlencode()

        return self.render(
            request,
            template="tears/nettsaker.html",
            context_overrides={
                "page_obj": page_obj,
                "all_posts": page_obj,
                "programs": ProgramPage.objects.live().order_by("title"),
                "categories": ProgramPage.CATEGORY_CHOICES,
                "selected_tema": selected_tema,
                "selected_programs": selected_programs,
                "selected_kategori": selected_kategori,
                "q": search_query,  # Pass search query to template
                "sort": sort_order,  # Pass sort order to template
                "total_article_count": total_article_count,
                "querystring": querystring,
            },
        )


class ProgrammerPage(Page):
    page_description = "This is the program list page of the website and has the content at https://radionova.no/programmer."
    subpage_types = ["ProgramPage"]
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]
    subpage_types = ["ProgramPage"]

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
        total_program_count = sum(
            len(programs) for programs in grouped_programs.values()
        )
        context["grouped_programs"] = grouped_programs
        context["total_program_count"] = total_program_count

        return context


from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from django import forms
from django.contrib.auth import get_user_model
from .blocks import CenteredFlexBlock  

class ProgramPage(Page):
    page_description = "This is the program page of the website and has the content at e.g. https://radionova.no/programmer/frokost."
    subpage_types = ["BlogPage"]

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
        [  # we are using Choices in since timeblock does not support choices every half hour. Its in blocks.py
            (
                "sendetid",
                blocks.StructBlock(
                    [
                        (
                            "weekday",
                            blocks.ChoiceBlock(
                                choices=Weekday.choices,
                                required=False,
                                help_text="Choose the day of the week",
                            ),
                        ),
                        (
                            "start_time",
                            blocks.ChoiceBlock(
                                choices=TimeChoices.choices,
                                required=False,
                                help_text="Start time",
                            ),
                        ),
                        (
                            "end_time",
                            blocks.ChoiceBlock(
                                choices=TimeChoices.choices,
                                required=False,
                                help_text="End time",
                            ),
                        ),
                    ]
                ),
            ),
        ],
        blank=True,
        verbose_name="Sendetider (Broadcast Times)",
    )

    #  Social Media Links
    instagram_link = models.URLField("Instagram-link", blank=True)
    facebook_link = models.URLField("Facebook-link", blank=True)
    tiktok_link = models.URLField("TikTok-link", blank=True)
    email_link = models.URLField("E-post-link", blank=True)

    description = StreamField(
        [
            ("image_with_description", ImageWithDescriptionBlock()),
            ("content", blocks.RichTextBlock()),
            ("flex_block", CenteredFlexBlock())
        ],
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("main_image"),
        FieldPanel("category"),
        FieldPanel("program"),
        FieldPanel("intro"),
        FieldPanel("sendetider"),
        
        FieldPanel("instagram_link"),
        FieldPanel("facebook_link"),
        FieldPanel("tiktok_link"),
        FieldPanel("email_link"),
        FieldPanel("description"),
    ]


class BlogPageAdminForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        # Call the parent class's __init__ method first
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:
            if self.for_user:
                self.initial["user"] = self.for_user.pk


class BlogPage(Page):
    page_description = "This is the blog page of the website and has the content at e.g. https://radionova.no/blog/2024/10/12/ny-blog."
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("Post time")
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    imageDecription = models.CharField(
        "Bildetekst på hovedbilde:",
        max_length=255,
        blank=True,
        help_text="Bildetekst under første bildet",
    )
    ingress = models.TextField(
        "Ingress",
        max_length=500,
        blank=True,
        help_text="Kort ingress/underoverskrift under tittelen",
    )
    overtittel = models.CharField(
        "Navn på det du andmelder/intervjuer",
        max_length=500,
        blank=True,
        help_text=" F.eks. '[Navn på festival]' eller '[Navn på artist]'.",
    )
    # this is for having nettsaker in programpages. makes it possible to show programs each nettsak they have made only

    imageDecription_placeholder = forms.TextInput(
        attrs={"placeholder": "Bildetekst på hovedbilde (valgfritt)"}
    )
    overtittel_placeholder = forms.TextInput(attrs={"placeholder": "(valgfritt)"})

    program = models.ForeignKey(
        "tears.ProgramPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_posts",
        verbose_name="Redaksjon",
    )
    typeArticle = models.CharField(
        max_length=50,
        choices=[
            ("article", "Artikkel"),
            ("anmeldelse", "Anmeldelse"),
            ("intervju", "Intervju"),
        ],
        default="article",
        verbose_name="Type of Article",
    )
    body = StreamField(
        [
            ("main_image", ImageChooserBlock()),
            ("image_with_description", ImageWithDescriptionBlock()),
            ("content", blocks.RichTextBlock()),
            ("flex_block", CenteredFlexBlock()),
        ],
        blank=True,
    )

    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("user"),
        FieldPanel("typeArticle"),
        FieldPanel("forfatter"),
        FieldPanel("ingress"),
        FieldPanel("overtittel", widget=overtittel_placeholder),
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("imageDecription", widget=imageDecription_placeholder),
    ]

    base_form_class = BlogPageAdminForm

    def save(self, *args, **kwargs):
        # Auto-assign user if not set
        if not self.user_id:
            User = get_user_model()
            # Get the current user from the request context
            # This requires passing the user during save
            if hasattr(self, "_user"):
                self.user = self._user
            else:
                # Fallback - you might want to set a default user or handle this differently
                self.user = User.objects.filter(is_staff=True).first()

        # Auto-assign program based on parent page
        if not self.program:
            parent = self.get_parent()
            if parent and parent.__class__.__name__ == "ProgramPage":
                self.program = parent

        super().save(*args, **kwargs)

    def related_posts(self):
        return (
            BlogPage.objects.live().filter(program=self.program).exclude(id=self.id)[:3]
        )


class FreeTextPage(Page):
    page_description = "These are pages with free text, can be used for additional pages like  /sendeplan, /a-lista etc."
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def serve(self, request):
        # Get the latest child AListaPage
        latest_post = (
            self.get_children()
            .live()
            .specific()
            .order_by("-first_published_at")
            .first()
        )
        if latest_post:
            return HttpResponseRedirect(latest_post.url)
        return super().serve(request)  # fallback if no child pages exist


class DagTidPage(Page):
    page_description = (
        "This page is for configuring DagTid, About Radio Nova, and Omtaler i medier."
    )

    # Free text for 'About Radio Nova' (top part)
    about_radio_nova = StreamField(
        [
            ("content", blocks.RichTextBlock()),
            ("main_image", ImageChooserBlock()),
            ("flex_block", CenteredFlexBlock()),
        ],
        blank=True,
        verbose_name="About Radio Nova",
    )

    # Repeating Employees
    ansatte = StreamField(
        [
            (
                "ansatt",
                blocks.StructBlock(
                    [
                        (
                            "name",
                            blocks.CharBlock(
                                required=True, help_text="Employee full name"
                            ),
                        ),
                        (
                            "role",
                            blocks.CharBlock(
                                required=True, help_text="Their role/title"
                            ),
                        ),
                        (
                            "email",
                            blocks.CharBlock(
                                required=False, help_text="Their email address"
                            ),
                        ),
                        ("image", ImageChooserBlock(required=False)),
                    ]
                ),
            ),
        ],
        blank=True,
        verbose_name="Ansatte (Employees)",
    )

    # Repeating Media Mentions
    omtaler_i_medier = StreamField(
        [
            (
                "omtale",
                blocks.StructBlock(
                    [
                        ("title", blocks.CharBlock(required=True)),
                        ("date", blocks.DateBlock(required=True)),
                        ("description", blocks.TextBlock(required=True)),
                        ("link", blocks.URLBlock(required=True)),
                        ("image", ImageChooserBlock(required=True)),
                    ]
                ),
            ),
        ],
        blank=True,
        verbose_name="Omtaler i andre medier",
    )

    content_panels = Page.content_panels + [
        FieldPanel("about_radio_nova"),
        FieldPanel("ansatte"),
        FieldPanel("omtaler_i_medier"),
    ]

    subpage_types = []


class AListaPage(
    Page
):  ##TODO: make it so only alista pages can be created under /a-lista/"
    page_description = "This page is for configuring A-lista for every week"
    forfatter = models.CharField("Forfatter", max_length=255, blank=True)
    ingress = models.TextField(blank=True, help_text="ingress")
    dato = models.DateField("Dato", blank=True, null=True, help_text="Dato for A-lista")

    program = models.ForeignKey(
        "tears.ProgramPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="a_lista_posts",
        verbose_name="Redaksjon",
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
        return (
            AListaPage.objects.live()
            .exclude(id=self.id)
            .order_by("-first_published_at")[:count]
        )


from django.utils.timezone import localtime, now
from datetime import datetime, time


class Sendeplan(Page):
    page_description = "This page is for configuring sendeplan for the semester"

    def get_context(self, request):
        context = super().get_context(request)

        programs = ProgramPage.objects.live().public().specific()
        sendeplan = {str(i): [] for i in range(1, 8)}  # 1=Mandag .. 7=Søndag

        current_time = localtime(now()).time()
        current_weekday = str(localtime(now()).isoweekday())

        # Create time slots mapping for proper positioning
        time_slots = ["00:00"] + [
            f"{hour:02d}:{minute:02d}" for hour in range(6, 24) for minute in (0, 30)
        ]

        def get_time_slot_index(time_str):
            """Get the index of a time slot in our time_slots array"""
            if not time_str:
                return 0
            try:
                return time_slots.index(time_str)
            except ValueError:
                # If exact match not found, find the closest earlier slot
                time_obj = datetime.strptime(time_str, "%H:%M").time()
                for i, slot in enumerate(time_slots):
                    slot_time = datetime.strptime(slot, "%H:%M").time()
                    if slot_time > time_obj:
                        return max(0, i - 1)
                return len(time_slots) - 1

        def calculate_rowspan(start_time_str, end_time_str):
            """Calculate rowspan considering the 00:00-06:00 gap"""
            if not start_time_str or not end_time_str:
                return 1

            start_time_obj = datetime.strptime(start_time_str, "%H:%M").time()
            end_time_obj = datetime.strptime(end_time_str, "%H:%M").time()

            # Handle overnight programs (crossing midnight)
            if end_time_obj <= start_time_obj:
                # Program goes past midnight
                if start_time_obj >= time(22, 0):  # Starts late evening
                    # Calculate from start to midnight, then from 06:00 to end
                    minutes_to_midnight = (24 * 60) - (
                        start_time_obj.hour * 60 + start_time_obj.minute
                    )

                    if end_time_obj <= time(6, 0):
                        # Ends before 06:00, so it spans the gap
                        return max(1, int(minutes_to_midnight / 30))
                    else:
                        # Ends after 06:00
                        minutes_from_6am = (
                            end_time_obj.hour * 60 + end_time_obj.minute - 6 * 60
                        )
                        total_minutes = minutes_to_midnight + minutes_from_6am
                        return max(1, int(total_minutes / 30))
                else:
                    # Normal case - shouldn't happen with proper data
                    return 1
            else:
                # Normal program within same day
                if start_time_obj < time(6, 0) and end_time_obj < time(6, 0):
                    # Both in the 00:00-06:00 range (mapped to single slot)
                    return 1
                elif start_time_obj >= time(6, 0) and end_time_obj >= time(6, 0):
                    # Both in the 06:00-24:00 range
                    duration_minutes = (
                        end_time_obj.hour - start_time_obj.hour
                    ) * 60 + (end_time_obj.minute - start_time_obj.minute)
                    return max(1, int(duration_minutes / 30))
                else:
                    # Spans across the gap - shouldn't happen with proper scheduling
                    return 1

        for program in programs:
            for block in program.sendetider:
                data = block.value
                weekday = data.get("weekday")
                if weekday:
                    start_time_str = data.get("start_time")
                    end_time_str = data.get("end_time")

                    start_time = (
                        datetime.strptime(start_time_str, "%H:%M").time()
                        if start_time_str
                        else None
                    )
                    end_time = (
                        datetime.strptime(end_time_str, "%H:%M").time()
                        if end_time_str
                        else None
                    )

                    is_now = False
                    if weekday == current_weekday and start_time and end_time:
                        if start_time <= current_time <= end_time:
                            is_now = True

                    # Calculate proper rowspan and position
                    rowspan = calculate_rowspan(start_time_str, end_time_str)
                    time_slot_index = get_time_slot_index(start_time_str)

                    sendeplan[weekday].append(
                        {
                            "page": program,
                            "title": program.title,
                            "start_time": start_time_str,
                            "end_time": end_time_str,
                            "category": program.get_category_display(),
                            "intro": program.intro,
                            "main_image": program.main_image,
                            "is_live_now": is_now,
                            "rowspan": rowspan,
                            "time_slot_index": time_slot_index,
                        }
                    )

        # Sort programs by start time for each day
        for day in sendeplan:
            sendeplan[day].sort(key=lambda x: x["time_slot_index"])

        # Create a proper grid structure to avoid positioning issues
        grid = {}
        for day_num in range(1, 8):
            day_str = str(day_num)
            grid[day_str] = {}

            # Track which time slots are occupied
            occupied_slots = set()

            for program in sendeplan[day_str]:
                start_index = program["time_slot_index"]
                rowspan = program["rowspan"]

                # Find the first available slot at or after the program's start time
                actual_start_index = start_index
                while actual_start_index in occupied_slots:
                    actual_start_index += 1

                # Mark slots as occupied
                for i in range(actual_start_index, actual_start_index + rowspan):
                    occupied_slots.add(i)

                # Update program's actual position
                program["actual_time_slot_index"] = actual_start_index
                grid[day_str][actual_start_index] = program

        context["day_names"] = [
            "Mandag",
            "Tirsdag",
            "Onsdag",
            "Torsdag",
            "Fredag",
            "Lørdag",
            "Søndag",
        ]
        context["sendeplan"] = sendeplan
        context["sendeplan_grid"] = grid
        context["occupied_cells"] = occupied_slots
        context["weekdays"] = ["1", "2", "3", "4", "5", "6", "7"]
        context["time_slots"] = time_slots

        # Find current live program
        current_program = None
        for day_programs in sendeplan.values():
            for program in day_programs:
                if program["is_live_now"]:
                    current_program = program
                    break
            if current_program:
                break

        if current_program:
            context["current_live_text"] = (
                f"Direkte: Radio Nova / {current_program['start_time']}–{current_program['end_time']}: {current_program['title']}"
            )
        else:
            context["current_live_text"] = "Direkte: Radio Nova"

        return context


# This is varslinger and other info put in text
from wagtail.snippets.models import register_snippet


@register_snippet
class TextContent(models.Model):
    title = models.CharField(max_length=255, default="Text Content")
    content = StreamField(
        [
            ("rich_text", blocks.RichTextBlock(label="Tekst")),
            ("quote", blocks.BlockQuoteBlock(label="Sitat")),
        ],
        blank=True,
        help_text="Hovedinnholdet i manualen",
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("content"),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Varsling"
        verbose_name_plural = "Varsling"


from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail import blocks

from wagtail.images.blocks import ImageChooserBlock


@register_snippet
class ManualCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=0, help_text="Sorteringsrekkefølge")

    panels = [
        FieldPanel("name"),
        FieldPanel("order"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manual Category"
        verbose_name_plural = "Manual Categories"
        ordering = ["order", "name"]


@register_snippet
class Manual(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        ManualCategory, on_delete=models.CASCADE, related_name="manuals"
    )
    description = models.TextField(blank=True, help_text="Kort beskrivelse av manualen")

    content = StreamField(
        [
            ("rich_text", blocks.RichTextBlock(label="Tekst")),
            ("quote", blocks.BlockQuoteBlock(label="Sitat")),
            (
                "code",
                blocks.TextBlock(label="Kode", help_text="For kode eller kommandoer"),
            ),
        ],
        blank=True,
        help_text="Hovedinnholdet i manualen",
    )
    order = models.IntegerField(
        default=0, help_text="Sorteringsrekkefølge innenfor kategori"
    )
    is_published = models.BooleanField(default=True, help_text="Synlig for brukere")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    panels = [
        FieldPanel("title"),
        FieldPanel("category"),
        FieldPanel("description"),
        FieldPanel("content"),
        FieldPanel("order"),
        FieldPanel("is_published"),
    ]

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    class Meta:
        verbose_name = "Manual"
        verbose_name_plural = "Manuals"
        ordering = ["category__order", "category__name", "order", "title"]


@register_snippet
class BeskjedFraDagtid(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tittel")

    text = StreamField(
        [
            ("text", blocks.RichTextBlock()),
        ],
        blank=True,
        verbose_name="Tekstinnhold",
        help_text="Innholdet som vises i panelet på dashbordet",
    )
    panels = [
        FieldPanel("title"),
        FieldPanel("text"),
    ]

    class Meta:
        verbose_name = "Beskjed fra dagtid"
        verbose_name_plural = "Beskjed fra dagtid"

    def __str__(self):
        return self.title
