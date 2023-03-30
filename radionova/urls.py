from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListCreatePostAPIView.as_view(), name='get_post_articles'),
    path('<int:pk>/', views.RetrieveUpdateDestroyPostAPIView.as_view(), name='get_delete_update_articles'),
]