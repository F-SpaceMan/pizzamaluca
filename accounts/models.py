from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Address(models.Model):
    street = models.TextField()
    number = models.IntegerField()
    zipCode = models.BigIntegerField()
    neighborhood = models.TextField()

#class Name(models.Model):
#    firstName = models.TextField()
#   middleName = models.TextField()
#    lastName = models.TextField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.BigIntegerField(primary_key=True)
    telephoneNumber = models.TextField()
    email = models.TextField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username