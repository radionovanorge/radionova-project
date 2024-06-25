from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Program, BroadcastSchedule


class BroadcastScheduleViewset(SnippetViewSet):
    model = BroadcastSchedule
    icon = "list-ul"
    menu_label = "Broadcast Schedule"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("program", "date", "start_time", "end_time")


class ProgramViewset(SnippetViewSet):
    model = Program
    icon = "list-ul"
    menu_label = "Programs"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "description")
    list_filter = ("name",)
    search_fields = ("name", "description")
