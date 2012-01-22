from datetime import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.views import generic

import forms
import models

class CompletedOrdersListView(generic.ListView):
    template_name = 'order/completed_orders.html'
    model = models.Order
    paginate_by = 10
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(CompletedOrdersListView, self).get_queryset()
        return queryset.exclude(time_closed=None)

    def render_to_response(self, context):
        if not self.request.user.is_superuser:
            raise PermissionDenied
        return super(CompletedOrdersListView, self).render_to_response(context)

class OrderStatusListView(generic.ListView):
    template_name = 'order/order_status.html'
    model = models.Order
    paginate_by = 10
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(OrderStatusListView, self).get_queryset()
        return queryset.filter(user=self.request.user)

def order_details(self, request, order_id,
        template_name='order/order_details.html'):
    order = get_object_or_404(models.Order, pk=order_id)
    if request.user != order.user:
        raise Exception, PermissionDenied

    return render_to_response(template_name, RequestContext(request, {
        'order': order
    }))

def api_order_info(request):
    """
    Returns JSON list of orders for passed-in order ids, if they exist and have
    been "placed."
    """
    id_list = []
    if request.GET:
        ids = request.GET.get('order_ids', None)
        if ids:
            try:
                id_list = [int(i) for i in ids.split(',')]
            except ValueError:
                raise Http404, _('Invalid id(s).')

    orders = models.Order.objects.filter(
        id__in=id_list).exclude(order_placed=None)
    data = {}
    for order in orders:
        if order.time_closed:
            time_closed = order.time_closed.strftime('%m/%d/%Y %I:%M%p')
        else:
            time_closed = False
        data['order-%s' % order.id] = {
            'seconds_elapsed': (datetime.now() - order.order_placed).seconds,
            'time_closed': time_closed
        }
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def complete_order(request, order_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    # Mark order complete at current time.
    order = get_object_or_404(models.Order, pk=order_id)
    order.time_closed = datetime.now()
    order.save()

    messages.success(request, _('Order `%s` marked complete.' % order))

    # Redirect back to same page.
    return HttpResponseRedirect(reverse('active_orders'))

def active_orders(request, template_name='order/active_orders.html'):
    orders = models.Order.objects.filter(
        time_closed=None).exclude(order_placed=None)
    if not request.user.is_superuser:
        raise PermissionDenied

    return render_to_response(template_name, RequestContext(request, {
        'orders': orders
    }))

def order_details(request, order_id, template_name='order/order_details.html'):
    order = get_object_or_404(models.Order, pk=order_id)
    return render_to_response(template_name, RequestContext(request, {
        'order': order
    }))

def checkout(request, template_name='order/checkout.html'):
    order = request.session.get('order', None)

    # If the order is empty, redirect to the home page.
    if not order or order.cost == 0:
        return HttpResponseRedirect(reverse('home'))

    if request.POST:
        order.user = request.user
        order.order_placed = datetime.now()
        order.save()
        request.session['order'] = None
        return HttpResponseRedirect(reverse('order_status'))
    else:
        return render_to_response(template_name,
            RequestContext(request, {
                'order': order
            })
        )

def home(request, template_name='order/index.html'):
    # Get the active order for the current user/session.
    # Since we're doing lazy registration, we store the active order in the
    # session.
    order = request.session.get('order', None)
    if not order:
        order = models.Order()
    instance = models.Pizza(order=order)

    if request.POST:
        form = forms.PizzaForm(request.POST, instance=instance)
    else:
        form = forms.PizzaForm(instance=instance)

    if form.is_valid():
        if not order.pk:
            order.save()
            pizza = form.save(commit=False)
            pizza.order = order
            pizza.save()
            form.save_m2m()
        else:
            pizza = form.save()
        request.session['order'] = order

        return HttpResponseRedirect(reverse('home'))

    else:
        return render_to_response(template_name,
            RequestContext(request, {
                'form': form,
                'order': order
            })
        )
