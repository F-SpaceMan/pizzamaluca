from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
import logging
from django import forms
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserProfileForm(UserCreationForm):
    class Meta:
       model = UserProfile
       fields = ("username","email","cpf","telephoneNumber",
                "street", "number", "zipCode", "neighborhood",
                "firstName", "middleName","lastName")
