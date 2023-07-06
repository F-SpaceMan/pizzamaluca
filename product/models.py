from django.db import models

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

    def __str__(self):
        return f'{self.description} - {[_.taste_name for _ in self.tastes.all()]}' 

class Drink(Product):
    volume = models.FloatField()

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
    total = models.FloatField()

    def __str__(self):
        return f'{self.id}'

class Address(models.Model):
    street = models.TextField()
    number = models.IntegerField()
    zipCode = models.BigIntegerField()
    neighborhood = models.TextField()

class Name(models.Model):
    firstName = models.TextField()
    middleName = models.TextField()
    lastName = models.TextField()

class User(models.Model):
    cpf = models.BigIntegerField(primary_key=True)
    telephoneNumber = models.TextField()
    email = models.TextField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    name =  models.ForeignKey(Name, on_delete=models.CASCADE)
    password = models.TextField()

class Order(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    itemList = models.ManyToManyField(Product)

    def __str__(self):
        return f'{self.id} - {self.itemList}'
    

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self) -> str:
        return f'Cart for {self.user.name}'
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
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
    
    def __str__(self) -> str:
        return f"{self.quantity} x {self.item_name}"
    
    

    # pizza = models.ManyToManyField(Pizza,blank=True, null=True)
    # drink = models.ManyToManyField(Drink,blank=True, null=True)
    # combo = models.ManyToManyField(Combo,blank=True, null=True)
    # pizza_quantity = models.IntegerField(Product,blank=True, null=True)
    # drink_quantity = models.IntegerField(Product,blank=True, null=True)
    # combo_quantity = models.IntegerField(Product,blank=True, null=True)