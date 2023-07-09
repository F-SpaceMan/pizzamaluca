from django.contrib import admin

# Register your models here.
from .models import Pizza, Drink, Combo, Taste, Cart, Item, CartItem, Order, OrderItem

admin.site.register(Pizza)
admin.site.register(Drink)
admin.site.register(Combo)
admin.site.register(Taste)
admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)


