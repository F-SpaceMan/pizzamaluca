from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.CharField(max_length=50, unique=True)

    cpf = models.BigIntegerField(unique=True)
    telephoneNumber = models.TextField(unique=True, null=True)

    firstName = models.TextField()
    middleName = models.TextField()
    lastName = models.TextField()

    street = models.TextField()
    number = models.IntegerField()
    zipCode = models.BigIntegerField()
    neighborhood = models.TextField()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = ["email","cpf","telephoneNumber",
                        "street", "number", "zipCode", "neighborhood",
                          "firstName", "middleName","lastName"]