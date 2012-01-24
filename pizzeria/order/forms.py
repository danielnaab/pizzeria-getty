from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField

from uni_form.helper import FormHelper
from uni_form import layout

import models

class PizzaForm(forms.ModelForm):
    # Make toppings a set of checkboxes:
    #toppings = forms.ModelMultipleChoiceField(
    #    queryset=models.Topping.objects.all(),
    #    widget=forms.CheckboxSelectMultiple
    #)

    class Meta:
        model = models.Pizza

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.MultiField(
                'Add a pizza to your order...',
                layout.Fieldset(
                    'Pizza type',
                    'size',
                    'crust_type',
                ),
                layout.Fieldset(
                    'Customize your pizza',
                    'toppings',
                ),
                layout.Div(
                    layout.HTML('<div>Special instructions:</div>'),
                    'do_not_cut',
                    'heavy_sauce',
                    'lite_bake',
                    'lite_cheese',
                    'lite_sauce',
                    'no_sauce',
                    'well_done',
                    css_id='special-instructions',
                ),
                'special_instructions',
                'entries'
            ),
            layout.ButtonHolder(
                layout.Submit('add-pizza', 'Add To Order'),
                layout.HTML('<div>Add this delicious pizza to your order now!</div>')
            )
        )
        return super(PizzaForm, self).__init__(*args, **kwargs)

class OrderForm(forms.ModelForm):
    zipcode = USZipCodeField()

    class Meta:
        model = models.Order
        exclude = (
            'user', 'order_placed', 'time_closed')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = layout.Layout(
            layout.MultiField(
                '<span class="alt">Delivery Details</span>',
                'address_1',
                'address_2',
                'city',
                'state',
                'zipcode',
                'phone_number',
                'delivery_instructions',
            ),
            layout.ButtonHolder(
                layout.Submit('confirm-order', 'Confirm Order'),
                layout.HTML("<div>You're one click closer to a tasty pie!</div>")
            )
        )
        return super(OrderForm, self).__init__(*args, **kwargs)
