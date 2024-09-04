
from django.urls import reverse


from wagtail import hooks
from wagtail.models import Site, Page
from wagtail.admin.menu import MenuItem

from wagtail.snippets.wagtail_hooks import SnippetsMenuItem
from django.templatetags.static import static
from django.utils.html import format_html

from .models import BlogPage


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("tears/js/base.js"))

@hooks.register("disable_password_changing")
def disable_password_changing(request, menu_items):
    if request.user.is_superuser:
        return
    return format_html('<script src="{}"></script>', static("tears/js/styles_for_normal_user.js"))


@hooks.register("construct_main_menu")
def rename_snippets_menu_item(request, menu_items):
    for item in menu_items:
        if isinstance(item, SnippetsMenuItem):
            item.label = "Programs"


@hooks.register("construct_main_menu")
def add_custom_menu_item(request, menu_items):
    # get group of current user
    user = request.user
    if not user.is_superuser:
        group = user.groups.first()
        default_site = Site.objects.get(is_default_site=True)

        create_new_page_id = default_site.root_page.get_children().filter(
            title=group.name
        ).first().id

        custom_menu_item = MenuItem(
            label="Write an article",
            url=reverse("wagtailadmin_pages:add", args=(
                "tears", "blogpage", create_new_page_id)),
            classnames="custom-button",
            icon_name="edit",
            order=0,
        )
        menu_items.append(custom_menu_item)


@ hooks.register("construct_main_menu")
def hide_some_menu_items(request, menu_items):
    items_to_remove = ["images", "documents", "help", "reports", "help"]
    items_to_remove = []
    menu_items[:] = [
        item for item in menu_items if item.name not in items_to_remove]


@ hooks.register("construct_settings_menu")
def hide_some_settings_menu_items(request, menu_items):
    items_to_remove = ["workflows", "workflow tasks", "collections"]
    menu_items[:] = [
        item for item in menu_items if item.name not in items_to_remove]


@ hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static(
            "tears/css/custom_admin.css")
    )
