from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^order-details/(?P<order_id>[\d]+)/$', views.order_details,
        name='order_details'),
    url(r'^order-status/$', views.OrderStatusListView.as_view(),
        name='order_status'),
    url(r'^active-orders/$', views.active_orders, name='active_orders'),
    url(r'^complete-order/(?P<order_id>[\d]+)/$', views.complete_order,
        name='complete_order'),
    url(r'^completed-orders/$', views.CompletedOrdersListView.as_view(),
        name='completed_orders'),

    url(r'^api/order-info/$', views.api_order_info, name='api_order_info'),
)
