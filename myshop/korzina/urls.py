from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.korzina_detail, name='korzina_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.korzina_add, name='korzina_add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.korzina_remove, name='korzina_remove'),
]