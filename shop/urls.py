from . import views
from django.urls import path

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('product/<slug:slug>', views.product_detail, name="product_detail"),
    path('category_products/<slug:slug>', views.category_products, name="category_products"),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name="cart_add"),
    # path('cart/remove/<int:product_id>/', views.remove_from_cart, name="cart_remove"),
    path('like/<slug:slug>/', views.toggle_like, name="toggle_like"),
    path('wishlist/', views.wishlist, name="wishlist"),
    path('cart/', views.cart_detail, name="cart_detail"),
    path('cart/add/<int:product_id>/', views.cart_add, name="cart_add"),
    path('cart/remove/<int:product_id>/', views.cart_remove, name="cart_remove"),
    path('cart/decrement/<int:product_id>/', views.cart_decrement, name="cart_decrement"),
    path('cart/clear/', views.cart_clear, name="cart_clear"),

]


