from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import (
    PhoneNumberField, USPostalCodeField, USStateField)
from django.db import models
from django.utils.translation import ugettext as _

from django_extensions.db.models import TimeStampedModel

class CustomerProfile(models.Model):
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = USStateField()
    zipcode = USPostalCodeField()
    phone_number = PhoneNumberField()

class Size(models.Model):
    label = models.CharField(max_length=64)
    inches = models.IntegerField()
    base_cost = models.DecimalField(max_digits=8, decimal_places=2)
    topping_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __unicode__(self):
        return '%d" %s - $%0.2f ($%0.2f/topping)' % (
            self.inches,
            self.label,
            self.base_cost,
            self.topping_cost
        )

class Topping(models.Model):
    label = models.CharField(max_length=64)
    is_vegan = models.BooleanField()

    def __unicode__(self):
        if self.is_vegan:
            return '%s (Vegan)' % self.label.title()
        else:
            return self.label.title()

class Order(TimeStampedModel):
    user = models.ForeignKey(User, null=True)
    delivery_instructions = models.TextField(null=True)
    order_placed = models.DateTimeField(null=True)
    time_closed = models.DateTimeField(null=True)

    class Meta:
        ordering = ('time_closed', '-order_placed',)

    def __unicode__(self):
        if self.user:
            return '%d Pizza(s) for %s' % (
                self.pizzas.all().count(),
                self.user.get_full_name() or self.user.username.title()
            )
        else:
            return '%d Pizza(s) - UNORDERED' % self.pizzas.all().count()

    @property
    def cost(self):
        """Calculates the cost of this pizza."""
        return sum([pizza.cost for pizza in self.pizzas.all()])

    @property
    def time_to_complete(self):
        """
        Returns the time used to close this order as a string in form HH:MM:SS,
        or the empty string.
        """
        if self.order_placed and self.time_closed:
            return ':'.join(['%02d' % float(part) for part in
                str(self.time_closed - self.order_placed).split(':')])
        else:
            return ''

class Pizza(TimeStampedModel):
    order = models.ForeignKey(Order, editable=False, related_name='pizzas')
    crust_type = models.IntegerField(
        choices=(
            (0, _('Cracker')),
            (1, _('Regular')),
            (2, _('Thick')),
            (3, _('Thin')),
            (4, _('Gluten-Free'))
        ),
        default=1
    )
    size = models.ForeignKey(Size)
    toppings = models.ManyToManyField(Topping, blank=True)

    # Options
    do_not_cut = models.BooleanField(default=False)
    heavy_sauce = models.BooleanField(default=False)
    lite_bake = models.BooleanField(default=False)
    lite_cheese = models.BooleanField(default=False)
    lite_sauce = models.BooleanField(default=False)
    no_sauce = models.BooleanField(default=False)
    well_done = models.BooleanField(default=False)

    special_instructions = models.CharField(
        max_length=128, null=True, blank=True,
        verbose_name=_('other instructions'))

    @property
    def cost(self):
        """Calculates the cost of this pizza."""
        return (self.size.base_cost
            + self.toppings.all().count() * self.size.topping_cost)

    def __unicode__(self):
        return '%s-Topping %s" %s Crust' % (
            self.toppings.count() or 'No',
            self.size.inches,
            self.get_crust_type_display(),
        )
