from django.shortcuts import render
from .forms import UserProfileForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserProfile


# Create your views here.
class SignUp(generic.CreateView):
    form_class = UserProfileForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

# @method_decorator(login_required, name='dispatch')
# class UserConfig(generic.TemplateView):

#     template_name = 'user/register.html'
#     # success_url = reverse_lazy('main_page')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["user_attributes"] = UserProfile.objects.filter(username=self.request.user.username).get()
#         return context