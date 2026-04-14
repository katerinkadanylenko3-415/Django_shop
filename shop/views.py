from urllib import request

import products
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .models import Product, Category

from django.contrib import messages


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(products, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop/product_list.html', {"page_obj": page_obj, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_products(request, slug):
    c = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=c).order_by("-created_at")
    return render(request, 'shop/product_list.html', {"products": products})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def toggle_like(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')

    product = get_object_or_404(Product, slug=slug)
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
    else:
        product.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


def wishlist(request):
    products = request.user.wishlist.all()
    return render(request, 'shop/product_list.html', {'products': products, 'title': 'My Wishlist'})


def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')

    products = request.user.wishlist.all()
    return render(request, 'shop/product_list.html', {
        'products': products,
        'wishlist_mode': True
    })




def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    messages.success(request, f"Товар {product.title} додано в кошик!")
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.warning(request, "Товар видалено з кошика")
    return redirect('cart_detail')

def cart_decrement(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product)
    return redirect('cart_detail')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Кошик очищено")
    return redirect('cart_detail')



