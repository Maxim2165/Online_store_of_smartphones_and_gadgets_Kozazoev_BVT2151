from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Korzina(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        korzina = self.session.get(settings.KORZINA_SESSION_ID)
        if not korzina:
            # save an empty korzina in the session
            korzina = self.session[settings.KORZINA_SESSION_ID] = {}
        self.korzina = korzina
        # сохранение текущего примененного купона
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.korzina:
            self.korzina[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.korzina[product_id]['quantity'] = quantity
        else:
            self.korzina[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Обновление сессии korzina
        self.session[settings.KORZINA_SESSION_ID] = self.korzina
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.korzina:
            del self.korzina[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.korzina.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.korzina[str(product.id)]['product'] = product

        for item in self.korzina.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.korzina.values())


    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.korzina.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.KORZINA_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()