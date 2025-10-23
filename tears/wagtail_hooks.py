from django.urls import reverse
from wagtail import hooks
from wagtail.models import Site, Page
from wagtail.admin.menu import MenuItem

from wagtail.snippets.wagtail_hooks import SnippetsMenuItem
from django.templatetags.static import static
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import TextContent


from django.http import JsonResponse
from .models import Manual, ManualCategory


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("tears/js/base.js"))


@hooks.register("disable_password_changing")
def disable_password_changing(request, menu_items):
    if request.user.is_superuser:
        return
    return format_html(
        '<script src="{}"></script>', static("tears/js/styles_for_normal_user.js")
    )


@hooks.register("construct_main_menu")
def rename_snippets_menu_item(request, menu_items):
    for item in menu_items:
        if isinstance(item, SnippetsMenuItem):
            item.label = "Administrer innhold"


# nettsak knapp for alle unntatt superuser
@hooks.register("construct_main_menu")
def add_custom_menu_item(request, menu_items):
    # get group of current user
    user = request.user
    if not user.is_superuser:
        group = user.groups.first()
        default_site = Site.objects.get(is_default_site=True)

        programmer_page = (
            default_site.root_page.get_children().filter(title="Programmer").first()
        )
        create_new_page_id = (
            programmer_page.get_children().filter(title=group.name).first().id
        )

        custom_menu_item = MenuItem(
            label="Write an article",
            url=reverse(
                "wagtailadmin_pages:add", args=("tears", "blogpage", create_new_page_id)
            ),
            classnames="custom-button",
            icon_name="edit",
            order=0,
        )
        menu_items.append(custom_menu_item)


# A-liste knapp bare for superuser
@hooks.register("construct_main_menu")
def add_custom_menu_item2(request, menu_items):
    if request.user.is_superuser:
        try:
            default_site = Site.objects.get(is_default_site=True)
            a_liste_page = (
                default_site.root_page.get_children().filter(title="A-lista").first()
            )
            if not a_liste_page:
                return

            custom_menu_item = MenuItem(
                label="Skriv en A-liste",
                url=reverse(
                    "wagtailadmin_pages:add",
                    args=("tears", "alistapage", a_liste_page.id),
                ),
                classnames="custom-button",
                icon_name="edit",
                order=0,
            )
            menu_items.insert(0, custom_menu_item)
        except Site.DoesNotExist:
            pass


@hooks.register("construct_main_menu")
def hide_some_menu_items(request, menu_items):
    items_to_remove = ["images", "documents", "help", "reports", "help"]
    items_to_remove = []
    menu_items[:] = [item for item in menu_items if item.name not in items_to_remove]


@hooks.register("construct_settings_menu")
def hide_some_settings_menu_items(request, menu_items):
    items_to_remove = ["workflows", "workflow tasks", "collections"]
    menu_items[:] = [item for item in menu_items if item.name not in items_to_remove]


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("tears/css/custom_admin.css")
    )


##varslinger/text_content og manual wagtail_hooks
# URL registrering - kun for visning
# wagtail_hooks.py


from .models import Manual, ManualCategory

# Kun en enkel visning av alle manualer


def manuals_index_view(request):
    """Hovedside for manualer - viser alle kategorier og manualer"""
    categories = ManualCategory.objects.prefetch_related("manuals").all()
    return render(
        request, "wagtailadmin/manuals/index.html", {"categories": categories}
    )


def manual_detail_view(request, manual_id):
    """Vis en spesifikk manual"""
    manual = Manual.objects.get(id=manual_id)
    return render(request, "wagtailadmin/manuals/detail.html", {"manual": manual})


# URL registrering - kun for visning
@hooks.register("register_admin_urls")
def register_manual_urls():
    return [
        path("manualer/", manuals_index_view, name="manuals-index"),
        path("manualer/<int:manual_id>/", manual_detail_view, name="manual-detail"),
    ]


# Meny registrering
@hooks.register("register_admin_menu_item")
def register_manuals_menu_item():
    return MenuItem(
        "Manualer", reverse("manuals-index"), icon_name="doc-full", order=400
    )


# varsling


def varsling_index_view(request):
    contents = TextContent.objects.all()
    return render(request, "wagtailadmin/varsling.html", {"contents": contents})


@hooks.register("register_admin_urls")
def register_varsling_urls():
    return [
        path("varsling/", varsling_index_view, name="varsling-index"),
    ]


@hooks.register("register_admin_menu_item")
def register_varsling_menu_item():
    return MenuItem(
        "Varsling",
        reverse("varsling-index"),
        icon_name="warning",
        order=500,
    )


# Beksjed fra dagtid
from .models import BeskjedFraDagtid
from wagtail.admin.ui.components import Component


class BeskjedPanel(Component):
    order = 100
    template_name = "wagtailadmin/home/partials/beskjed_panel.html"

    def get_context_data(self, parent_context):
        return {"beskjed": BeskjedFraDagtid.objects.first()}


@hooks.register("construct_homepage_panels")
def add_beskjed_panel(request, panels):
    panels.append(BeskjedPanel())

# Reservasjonsmeny knapp



class ExternalMenuItem(MenuItem):
    def render_html(self, request):
        return f'<a href="{self.url}" class="icon icon-{self.icon_name}" target="_blank" rel="noopener noreferrer">{self.label}</a>'

@hooks.register("register_admin_menu_item")
def register_reservasjon_menu_item():
    return ExternalMenuItem(
        "Reservasjon",
        "http://reservasjon.radionova.no/day.php?year=2025&month=10&day=23&area=3&room=63",
        icon_name="calendar-alt",
        order=501,
    )