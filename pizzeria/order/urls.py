from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^checkout/$',
        login_required(views.checkout),
        name='checkout'),
    url(r'^order-details/(?P<order_id>[\d]+)/$',
        login_required(views.order_details),
        name='order_details'),
    url(r'^order-status/$',
        login_required(views.OrderStatusListView.as_view()),
        name='order_status'),
    url(r'^active-orders/$',
        login_required(views.active_orders),
        name='active_orders'),
    url(r'^complete-order/(?P<order_id>[\d]+)/$',
        login_required(views.complete_order),
        name='complete_order'),
    url(r'^completed-orders/$',
        login_required(views.CompletedOrdersListView.as_view()),
        name='completed_orders'),
    url(r'^api/order-info/$',
        login_required(views.api_order_info),
        name='api_order_info'),
)
