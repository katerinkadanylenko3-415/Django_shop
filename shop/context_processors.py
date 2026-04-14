from .models import Category

def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }

from .cart import Cart

def cart_processor(request):
    return {'cart': Cart(request)}