from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from korzina.forms import korzinaAddProductForm



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    korzina_product_form = korzinaAddProductForm()
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'korzina_product_form': korzina_product_form})

