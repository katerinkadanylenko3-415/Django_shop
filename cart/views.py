from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')



@require_POST
def add_to_cart_ajax(request):
    product_id = request.POST.get('product_id')

    if not product_id:
        return JsonResponse({'error': 'No product_id'}, status=400)

    product = get_object_or_404(Product, id=product_id)

    cart = Cart(request)
    cart.add(product=product, quantity=1)

    return JsonResponse({
        'cart_count': len(cart)
    })