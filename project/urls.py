from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static


from project import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Radionova API",
        default_version="v1",
        description="First version of the Radionova API",
        terms_of_service="",
        contact=openapi.Contact(email="info@radionova.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = "Radionova Admin"
admin.site.site_title = "Radionova Admin Portal"
admin.site.index_title = "Radionova"
# urls
urlpatterns = [
    path("api/v1/articles/", include("radionova.urls")),
    path("admin/", admin.site.urls),
    path(
        "playground/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
