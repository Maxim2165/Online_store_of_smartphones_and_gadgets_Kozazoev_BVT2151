from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from korzina.korzina import Korzina


def order_create(request):
    korzina = Korzina(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if korzina.coupon:
                order.coupon = korzina.coupon
                order.discount = korzina.coupon.discount
            order.save()
            for item in korzina:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            korzina.clear()
            return render(request, 'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'korzina': korzina, 'form': form})