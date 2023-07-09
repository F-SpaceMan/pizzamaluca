from django.db import models
# from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Taste(models.Model):
    # id = models.AutoField(primary_key=True)
    taste_name = models.TextField()
    def __str__(self):
        return f'{self.taste_name}' 

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pizza(Product):
    # taste_enum = (
    #     ('Napolitan', "Napolitan"),
    #     ('Roman', "Roman"),
    #     ('Portuguese', "Portuguese")
    # )

    tastes = models.ManyToManyField(Taste)

    @property
    def i_price(self):
        return self.price

    def __str__(self):
        return f'{self.description} - {[_.taste_name for _ in self.tastes.all()]}' 

class Drink(Product):
    volume = models.FloatField()

    @property
    def i_price(self):
        return self.price
       

    def __str__(self):
        return f'{self.description} - {self.volume} l' 
    

class Item(models.Model):

    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.IntegerField()

    @property
    def item_name(self):
        if self.pizza:
            return self.pizza.description
        elif self.drink:
            return self.drink.description
        return ''
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.item_name}"
    
    
class Combo(Product):
    item = models.ManyToManyField(Item)

    @property
    def i_price(self):
        return self.price

    @property
    def combo_name(self):
        c_name = ''
        for _ in self.item.all():
            c_name = f'{_} + {c_name}'
        
        return c_name[:len(c_name)-2]

    def __str__(self):
        return f'{self.combo_name}'



class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    @property
    def item_name(self):
        if self.pizza:
            return self.pizza.description
        elif self.drink:
            return self.drink.description
        elif self.combo:
            return self.combo.description
        return ''
    
    @property
    def item_id(self):
        if self.pizza:
            return self.pizza.id
        elif self.drink:
            return self.drink.id
        elif self.combo:
            return self.combo.id
        return ''
    
    @property
    def total_value(self):
        if self.pizza:
            return self.pizza.price * self.quantity
        elif self.drink:
            return self.drink.price * self.quantity
        elif self.combo:
            return self.combo.price * self.quantity
        return ''

    def __str__(self) -> str:
        return f"{self.quantity} x {self.item_name}"

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Cart for {self.user.username}'
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    @property
    def item_name(self):
        if self.pizza:
            return self.pizza.description
        elif self.drink:
            return self.drink.description
        elif self.combo:
            return self.combo.description
        return ''
    
    @property
    def item_id(self):
        if self.pizza:
            return self.pizza.id
        elif self.drink:
            return self.drink.id
        elif self.combo:
            return self.combo.id
        return ''

    def __str__(self) -> str:
        return f"{self.quantity} x {self.item_name}"
    
    