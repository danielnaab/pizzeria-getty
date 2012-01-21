import collections

from django.core.management.base import BaseCommand

from pizzeria.order import models

def add_sizes():
    for label, inches, base_cost, topping_cost in (
            ('Extra Large', 16, 13.95, 2.25),
            ('Large', 14, 11.95, 1.85),
            ('Medium', 12, 9.95, 1.50),
            ('Small', 10, 7.95, 1.25)
        ):
        models.Size.objects.get_or_create(
            label=label,
            inches=inches,
            base_cost=base_cost,
            topping_cost=topping_cost
        )

def add_toppings():
    for label, is_vegan in (
            ('Alfredo Sauce', False),
            ('Anchovies', False),
            ('Artichoke Hearts', False),
            ('Bacon', False),
            ('Banana Peppers', False),
            ('Basil', False),
            ('BBQ Sauce', True),
            ('Beef', False),
            ('Black Olives', False),
            ('Bleu Cheese', False),
            ('Brats', False),
            ('Breakfast Sausage', False),
            ('Broccoli', False),
            ('Canadian Bacon', False),
            ('Cheddar', False),
            ('Chicken', False),
            ('Chicken Strips', False),
            ('Chorizo', False),
            ('Chunky Marinara Sauce', False),
            ('Cilantro', False),
            ('Classic Italian Sauce', True),
            ('Corn', False),
            ('Cucumbers', False),
            ('Diced Pickles', False),
            ('Dijon Kraut', False),
            ('Extra Cheese', False),
            ('Extra Spices', False),
            ('Feta', False),
            ('Garlic', False),
            ('Grated Parmesan', False),
            ('Green Olives', False),
            ('Green Peppers', False),
            ('Ham', False),
            ('Hashbrown', False),
            ('Honey Mustard', False),
            ('Hot Marinara Sauce', False),
            ('House Blend Cheese', False),
            ('Hummus', False),
            ('Jalapeno', False),
            ('Meatballs', False),
            ('Mozzarella', False),
            ('Mushroom', False),
            ('Peanut Sauce', True),
            ('Pepperoncini', False),
            ('Pepperoni', False),
            ('Pesto Sauce', True),
            ('Pineapple', False),
            ('Provolone', False),
            ('Ranch', False),
            ('Red Onion', False),
            ('Red Peppers', False),
            ('Ricotta Sauce', False),
            ('Ricotta Topping', False),
            ('Romano', False),
            ('Salami', False),
            ('Salsa', False),
            ('Sauerkraut', False),
            ('Sausage', False),
            ('Sauteed Yellow Onions', False),
            ('Spices', False),
            ('Spinach', False),
            ('Sprouts', False),
            ('Swiss', False),
            ('Tex-Mex', False),
            ('Tomatoes', False),
            ('Turkey', False),
            ('Walnuts', False),
            ('Wedge Fries', False),
            ('Yellow Onion', False)
        ):
        models.Topping.objects.get_or_create(label=label, is_vegan=is_vegan)

class Command(BaseCommand):
    help = 'Populates test pizza data into the database.'

    def handle(self, *args, **options):
        add_sizes()
        add_toppings()
