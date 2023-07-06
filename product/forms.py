from django import forms
from django_filters import BooleanFilter
from .models import Pizza, Drink, Combo,  Cart, User, CartItem

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, product):
        return "%s" % product.id


class CartForm(forms.ModelForm):

    checked_pizza = None
    checked_combo = None
    checked_drink = None

    class Meta:
        model = Cart
        fields = ('user', 'pizza', 'drink', 'combo')

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None)

        super(CartForm, self).__init__(*args, **kwargs)
        global checked_pizza, checked_drink, checked_combo

        checked_pizza = Pizza.objects.filter(
            id = self.request.user.id
        )
        checked_drink = Pizza.objects.filter(
            id = self.request.user.id
        )
        checked_combo = Pizza.objects.filter(
            id = self.request.user.id
        )
        # checked_pizza = BooleanFilter(field_name='pizza', lookup_expr='isnull', user = self.request.user)
        # checked_combo = BooleanFilter(field_name='combo', lookup_expr='isnull', user = self.request.user)
        # checked_drink = BooleanFilter(field_name='drink', lookup_expr='isnull', user = self.request.user)

        logger.debug('pizza')
        logger.debug([_ for _ in checked_pizza])
        logger.debug('drink')
        logger.debug([_ for _ in checked_drink])
        logger.debug('combo')
        logger.debug([_ for _ in checked_combo])
        # self.fields['pizza', 'drink',
        #             'combo', 'pizza_quantity',
        #             'drink_quantity', 'combo_quantity'].queryset=Cart.objects.filter(
        #                 user = self.request.user
        #             )

        for pizza in Pizza.objects.all():
            self.fields[f'pizza_{pizza.id}_quantity'] = forms.IntegerField(
                label=pizza.description,
                min_value=1,
                initial=1,
                required=False
            )

        for drink in Drink.objects.all():
            self.fields[f'drink_{drink.id}_quantity'] = forms.IntegerField(
                label=drink.description,
                min_value=1,
                initial=1,
                required=False
            )

        for combo in Combo.objects.all():
            self.fields[f'combo_{combo.id}_quantity'] = forms.IntegerField(
                label=combo.description,
                min_value=1,
                initial=1,
                required=False
            )

    # pizza_quantity = forms.IntegerField(min_value=1, initial=1,required=False)
    # drink_quantity = forms.IntegerField(min_value=1, initial=1,required=False)
    # combo_quantity = forms.IntegerField(min_value=1, initial=1,required=False)

    

    pizza = forms.ModelMultipleChoiceField(
        initial=[checked_pizza],
        queryset=Pizza.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    drink = forms.ModelMultipleChoiceField(
        queryset=Drink.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    combo = forms.ModelMultipleChoiceField(
        queryset=Combo.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def save(self, commit=True):
        cart = super(CartForm, self).save(commit=False)
        if commit:
            cart.save()

        for field_name, field_value in self.cleaned_data.items():
            if field_value and field_name.endswith('_quantity'):
                item_id = field_name.split('_')[1]
                item_type = field_name.split('_')[0]
                quantity = field_value

                cart_item = CartItem(
                    cart=cart,
                    quantity=quantity
                )

                if item_type == 'pizza':
                    cart_item.pizza = Pizza.objects.get(id=item_id)
                elif item_type == 'drink':
                    cart_item.drink = Drink.objects.get(id=item_id)
                elif item_type == 'combo':
                    cart_item.combo = Combo.objects.get(id=item_id)

                cart_item.save()

        return cart

    # def __init__(self, *args, **kwargs):
    #     super(CartForm, self).__init__(*args, **kwargs)
    #     self.fields['user'].required = False
    #     self.fields['pizza'].required = False
    #     self.fields['drink'].required = False
    #     self.fields['combo'].required = False