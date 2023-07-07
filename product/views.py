from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Pizza, Drink, Combo, Order, Cart
from django.shortcuts import get_object_or_404
from .forms import CartForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class ProducService(View):
    def calculatePizzaPrice(request):
        flavors = request.POST.getlist('flavors')
    
        price_per_flavor = 5.99
        total_price = len(flavors) * price_per_flavor
        
        return total_price



# def createOrder(request):
#     if request.method == 'POST':
#         # Assuming you have a form with relevant order information
#         form = OrderForm(request.POST)
        
#         if form.is_valid():
#             # Create a new Order instance
#             order = form.save(commit=False)
            
#             # Assign the current user as the order's user
#             order.user = request.user
            
#             # Save the order to the database
#             order.save()
            
#             # Redirect to a success page or perform any other desired action
#             return redirect('order_success')
#     else:
#         form = OrderForm()
    
#     context = {'form': form}
#     return render(request, 'create_order.html', context)

# def searchOrderByCPF(request):
#     if request.method == 'POST':
#         cpf = request.POST.get('cpf')
#         orders = Order.objects.filter(user__profile__cpf=cpf)
        
#         context = {'orders': orders}
#         return render(request, 'search_order.html', context)
    
#     return render(request, 'search_order.html')

def getTotalPriceOrder(request):
    return None
def getTotalOfProductsOrder(request):
    return None
def getOrderList(request):
    return None


@method_decorator(login_required, name='dispatch')
class MainView(TemplateView):
    template_name = 'main/mainPage.html'


@method_decorator(login_required, name='dispatch')
class CartView(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'product/menuPage.html'
    success_url = reverse_lazy('cart_page')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
@method_decorator(login_required, name='dispatch')
class ClosedCartView(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'order/cartPage.html'
    success_url = reverse_lazy('cart_page')

    def get_form_kwargs(self):
        """ Passa o objeto request object a classe de form
         Para mostrar apenas pedidos que pertencem ao user autenticado"""

        kwargs = super(ClosedCartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

# def clearCar(request):
#     del request.session['cart']
#     return redirect('cart_cleared')

# def product(request):
#     return HttpResponse('Hello World!')


# def yname(request, name):
#     return render(request, 'name/yname.html', {'namehtml':name})