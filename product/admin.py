from django.contrib import admin

# Register your models here.
from .models import Pizza, Drink, Combo, Taste, Cart, User, Name, Address, Item

admin.site.register(Pizza)
admin.site.register(Drink)
admin.site.register(Combo)
admin.site.register(Taste)
admin.site.register(Cart)
admin.site.register(User)
admin.site.register(Name)
admin.site.register(Address)
admin.site.register(Item)

