from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart


@login_required  # 6. Захист авторизацією
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # 5. Автоматично request.user
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()

            messages.success(request, f"Замовлення {order.order_number} успішно створено!")
            return render(request, 'order/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})



@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)  # Тільки свої замовлення
    return render(request, 'order/user_orders.html', {'orders': orders})



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})

