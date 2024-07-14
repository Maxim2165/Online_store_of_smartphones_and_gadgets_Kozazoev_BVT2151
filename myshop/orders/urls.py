from django.conf.urls import url
from . import views
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    url(_(r'^create/$'), views.order_create, name='order_create'),
]
