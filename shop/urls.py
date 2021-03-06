from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^shop/capi/', views.capi, name='capi'),
    url(r'^shop/test_api/', views.TestApi.as_view(), name='test_api'),
    url(r'^shop/order-success/$', views.CartOrder.as_view(), name='order-success'),
    url(r'^shop/order-success-post/', views.PostOrder.as_view(), name='order-success-post'),
    url(r'^shop/cart/$', views.CartView.as_view(), name='cart_list'),
    # url(r'^shop/cart/order$', views.CartOrder, name='cart_order'),
    url(r'^shop/$', views.ListView.as_view(), name='list_all'),
    url(r'^shop/(?P<slug>[-\w]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^shop/(?P<slug>[-\w]+)/brand/(?P<brand>[0-9]*)/$', views.DetailView.as_view(), name='detail_filter'),
    url(r'^shop/(?P<slug_category>[-\w]+)/product/(?P<slug>[-\w]+)/$', views.ProductView.as_view(), name='product'),
    url(r'^shop/search$', views.SearchListView.as_view(), name='list_search'),
    url(r'^shop/order-pay/(?P<order_id>[0-9]*)/$', views.PayView.as_view(), name='order-pay'),
    url(r'^shop/order-success-pay/', views.orderseccespay, name='order-secces-pay'),
]
