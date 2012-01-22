from django import forms

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
