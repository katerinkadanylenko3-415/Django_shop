from django.contrib.auth import user_login_failed

from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="home"),
    path('contacts/', views.contacts, name="contacts"),
    path('post/<slug:slug>/', views.post_detail, name="post_detail"),
    path('category/<slug:slug>', views.category, name="category"),
    path('tag/<slug:slug>/', views.tag_posts, name="tag_posts"),
    path('search/', views.search, name="search"),
    path('create-post/', views.create_post, name="create_post"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('post/<slug:slug>/delete/', views.delete_post, name="delete_post"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile_view, name="profile"),
    path('subscribe/', views.subscribe, name="subscribe"),


]
