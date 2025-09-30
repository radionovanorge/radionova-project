from django.urls import path
from .views import HamView

urlpatterns = [
    path(
        "sendeplan/", HamView.as_view(template="tears/sendeplan.html"), name="sendeplan"
    ),
    path(
        "programmer/",
        HamView.as_view(template="tears/programmer.html"),
        name="programmer",
    ),
]
