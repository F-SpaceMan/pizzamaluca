from django import forms
from django_filters import BooleanFilter
from .models import Pizza, Drink, Combo,  Cart, CartItem
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
    


# class CartForm(forms.ModelForm):
#     global checked_pizza, checked_drink, checked_combo

#     checked_pizza = []
#     checked_combo = []
#     checked_drink = []
    
#     class Meta:
#         model = Cart
#         fields = ('pizza', 'drink', 'combo')

#     def __init__(self, *args, **kwargs):

#         checked_pizza = []
#         checked_combo = []
#         checked_drink = []

#         self.request = kwargs.pop('request', None)

#         super(CartForm, self).__init__(*args, **kwargs)
        
        
#         checked = [_ for _ in CartItem.objects.filter(
#             user = self.request.user
#         )]

#         logger.debug('chek')

#         logger.debug([_ for _ in checked])


#         for pizza in Pizza.objects.all():
#             if pizza.id in [_.item_id for _ in checked]:
#                 logger.debug(pizza)
#                 checked_pizza.append(pizza.id)
#             self.fields[f'pizza_{pizza.id}_quantity'] = forms.IntegerField(
#                 label=pizza.description,
#                 min_value=1,
#                 initial=1,
#                 required=False
#             )

#         for drink in Drink.objects.all():
#             if drink.id in [_.item_id for _ in checked]:
#                 logger.debug(drink)
#                 checked_drink.append(drink.id)
#             self.fields[f'drink_{drink.id}_quantity'] = forms.IntegerField(
#                 label=drink.description,
#                 min_value=1,
#                 initial=1,
#                 required=False
#             )

#         for combo in Combo.objects.all():
#             if combo.id in [_.item_id for _ in checked]:
#                 logger.debug(combo)
#                 checked_combo.append(combo.id)
#             self.fields[f'combo_{combo.id}_quantity'] = forms.IntegerField(
#                 label=combo.description,
#                 min_value=1,
#                 initial=1,
#                 required=False
#             )

#     # pizza_quantity = forms.IntegerField(min_value=1, initial=1,required=False)
#     # drink_quantity = forms.IntegerField(min_value=1, initial=1,required=False)
#     # combo_quantity = forms.IntegerField(min_value=1, initial=1,required=False)

#     pizza = forms.ModelMultipleChoiceField(
#         initial=checked_pizza,
#         queryset=Pizza.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     drink = forms.ModelMultipleChoiceField(
#         initial=checked_drink,
#         queryset=Drink.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     combo = forms.ModelMultipleChoiceField(
#         initial=checked_combo,
#         queryset=Combo.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )

#     def save(self, commit=True):
#         cart = super(CartForm, self).save(commit=False)
#         if self.request.user.is_authenticated:
#             cart.user = self.request.user
#         if commit:
#             cart.save()

#         # Clear existing cart items for the current user
#         CartItem.objects.filter(user=self.request.user).delete()

#         for field_name, field_value in self.cleaned_data.items():
#             if field_name.startswith('pizza_') and field_value:
#                 item_id = field_name.split('_')[1]
#                 quantity = field_value
#                 pizza = get_object_or_404(Pizza, id=item_id)
#                 CartItem.objects.create(user=self.request.user, pizza=pizza, quantity=quantity)

#             elif field_name.startswith('drink_') and field_value:
#                 item_id = field_name.split('_')[1]
#                 quantity = field_value
#                 drink = get_object_or_404(Drink, id=item_id)
#                 CartItem.objects.create(user=self.request.user, drink=drink, quantity=quantity)

#             elif field_name.startswith('combo_') and field_value:
#                 item_id = field_name.split('_')[1]
#                 quantity = field_value
#                 combo = get_object_or_404(Combo, id=item_id)
#                 CartItem.objects.create(user=self.request.user, combo=combo, quantity=quantity)

#         return cart

    # def __init__(self, *args, **kwargs):
    #     super(CartForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].required = False
    #     self.fields['pizza'].required = False
    #     self.fields['drink'].required = False
    #     self.fields['combo'].required = False