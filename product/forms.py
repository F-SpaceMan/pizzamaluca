from django import forms
from django_filters import BooleanFilter
from .models import Pizza, Drink, Combo,  Cart, CartItem, Order, OrderItem
from django.shortcuts import get_object_or_404
from django.http import Http404

from django.forms import formset_factory

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CartForm(forms.ModelForm):
    pizza = forms.ModelMultipleChoiceField(queryset=Pizza.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    drink = forms.ModelMultipleChoiceField(queryset=Drink.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())
    combo = forms.ModelMultipleChoiceField(queryset=Combo.objects.all(), required=False, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Cart
        fields = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CartForm, self).__init__(*args, **kwargs)

        self.item_quantity_fields = {}

        self.initialize_item_fields(Pizza, 'pizza')
        self.initialize_item_fields(Drink, 'drink')
        self.initialize_item_fields(Combo, 'combo')

        self.set_initial_values()


    def initialize_item_fields(self, model_class, field_name):
        items = model_class.objects.all()
        # choices = [(item.id, str(item)) for item in items]

        for item in items:
            field_id = f'{field_name}_{item.id}_quantity'
            self.item_quantity_fields[field_id] = forms.IntegerField(
                min_value=1,
                label=item.description,
                required=False,
                widget=forms.NumberInput(attrs={'class': 'quantity-input', 'type':'number'})
            )
            self.fields[field_id] = self.item_quantity_fields[field_id]

    def set_initial_values(self):
        cart_items = CartItem.objects.filter(user=self.request.user)

        selected_pizza = {}
        selected_drink = {}
        selected_combo = {}

        for item in cart_items:
            if item.pizza:
                field_id = f'pizza_{item.pizza.id}_quantity'
                if item.pizza.id in selected_pizza:
                    selected_pizza[item.pizza.id] += item.quantity
                else:
                    selected_pizza[item.pizza.id] = item.quantity
                self.initial[field_id] = selected_pizza[item.pizza.id]
            elif item.drink:
                field_id = f'drink_{item.drink.id}_quantity'
                if item.drink.id in selected_drink:
                    selected_drink[item.drink.id] += item.quantity
                else:
                    selected_drink[item.drink.id] = item.quantity
                self.initial[field_id] = selected_drink[item.drink.id]
            elif item.combo:
                field_id = f'combo_{item.combo.id}_quantity'
                if item.combo.id in selected_combo:
                    selected_combo[item.combo.id] += item.quantity
                else:
                    selected_combo[item.combo.id] = item.quantity
                self.initial[field_id] = selected_combo[item.combo.id]

        self.initial['pizza'] = list(selected_pizza.keys())
        self.initial['drink'] = list(selected_drink.keys())
        self.initial['combo'] = list(selected_combo.keys())

    def is_valid(self):
        form_valid = super(CartForm, self).is_valid()
        return form_valid

    def save(self, commit=True):
        if self.request.user.is_authenticated:
            user = self.request.user
            cart, created = Cart.objects.get_or_create(user=user)
            CartItem.objects.filter(user=user).delete()
        else:
            # Handle anonymous user cart logic here
            return None

        self.instance = cart

        super(CartForm, self).save(commit=commit)

        self.create_cart_items(cart, 'pizza')
        self.create_cart_items(cart, 'drink')
        self.create_cart_items(cart, 'combo')

        logger.debug([s for s in self.cleaned_data])

        return cart


    def create_cart_items(self, cart, field_name):
        selected_items = self.cleaned_data[field_name]
        
        quantity_fields = self.get_quantity_fields(field_name)

        for item in selected_items:
            quantity_field = quantity_fields.get(f'{field_name}_{item.id}_quantity')
            if quantity_field is not None and isinstance(quantity_field, int) and quantity_field > 0:
                CartItem.objects.create(
                    user=self.request.user,
                    cart=cart,
                    quantity=quantity_field,
                    **{field_name: item}
                )


    def get_quantity_fields(self, field_name):
        quantity_fields = {}
        for field_id, field in self.item_quantity_fields.items():
            if field_id.startswith(field_name):
                quantity_fields[field_id] = self.cleaned_data.get(field_id)
        return quantity_fields
    

class ClosedCartForm(CartForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    def save(self, commit=True):
        if self.request.user.is_authenticated:
            user = self.request.user

            order = Order.objects.create(user=user)
            OrderItem.objects.filter(order=order).delete()
            
        else:
            # Handle anonymous user cart logic here
            return None

        
        self.instance = order

        super(ClosedCartForm, self).save(commit=commit)

        self.create_order_item(order, 'pizza')
        self.create_order_item(order, 'drink')
        self.create_order_item(order, 'combo')

        Cart.objects.filter(user=self.request.user).delete()

        return order


    def create_order_item(self, order, field_name):
        selected_items = self.cleaned_data[field_name]
        
        quantity_fields = self.get_quantity_fields(field_name)

        for item in selected_items:
            quantity_field = quantity_fields.get(f'{field_name}_{item.id}_quantity')
            if quantity_field is not None and isinstance(quantity_field, int) and quantity_field > 0:
                logging.debug('\n\n\n\n')
                logging.debug(order)
                logging.debug(item)
                logging.debug(quantity_field)
                logging.debug(order)
                logging.debug('\n\n\n\n')
                
                OrderItem.objects.create(
                    order=order,
                    **{field_name: item},
                    quantity=quantity_field
                )
