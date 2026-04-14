from shop.models import Category


def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }


def cart_context(request):
    cart = request.session.get('cart', {})

    cart_count = sum(
        item['quantity'] for item in cart.values()
    ) if cart else 0

    return {
        'cart_count': cart_count
    }

