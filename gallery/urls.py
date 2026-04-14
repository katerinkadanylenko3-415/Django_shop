
from . import views
from django.urls import path

urlpatterns = [
    path('', views.gallery_list, name="gallery"),
    path('gallery/', views.upload, name="upload"),

]