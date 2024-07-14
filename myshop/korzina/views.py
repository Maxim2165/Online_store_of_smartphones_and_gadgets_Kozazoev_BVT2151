from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .korzina import Korzina
from .forms import korzinaAddProductForm
from coupons.forms import CouponApplyForm


@require_POST
def korzina_add(request, product_id):
    korzina = Korzina(request)
    product = get_object_or_404(Product, id=product_id)
    form = korzinaAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        korzina.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('korzina:korzina_detail')

def korzina_remove(request, product_id):
    korzina = Korzina(request)
    product = get_object_or_404(Product, id=product_id)
    korzina.remove(product)
    return redirect('korzina:korzina_detail')

def korzina_detail(request):
    korzina = Korzina(request)
    for item in korzina:
        item['update_quantity_form'] = korzinaAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'korzina/detail.html',
                  {'korzina': korzina,
                   'coupon_apply_form': coupon_apply_form})