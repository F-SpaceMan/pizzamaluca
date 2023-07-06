from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .models import Pizza, Drink, Combo, Order, Cart
from django.shortcuts import get_object_or_404
from .forms import CartForm
from django.urls import reverse_lazy

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# class ProductController(View):
#     def getAllPizza(request):
#         return render(
#             request,
#             'product/menuPage.html',
#             {
#                 'allPizza':Pizza.objects.all(),
#             }
#         )
#     def getAllDrinks(request):
#         return render(
#             request,
#             'product/menuPage.html',
#             {
#                 'allDrink':Drink.objects.all(),
#             }
#         )
#     def getAllCombo(request):
#         return render(
#             request,
#             'product/menuPage.html',
#             {
#                 'allCombo':Combo.objects.all(),
#             }
#         )

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

# def getCart(request, userid):
#     cart = get_object_or_404(Cart, user.cpf=userid)
#     return render(request, 'product/cartPage.html', {'cart':cart})

class CartView(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'product/menuPage.html'
    success_url = reverse_lazy('menu_page')

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
# def newCart(request):
#     logger = logging.getLogger(__name__)

#     if request.method == 'POST':
#         form = CartForm(request.POST)
        
#         if form.is_valid():
#             cart = form.save(commit=False)
#             cart.user = None
#             cart.pizza_quantity = form.cleaned_data['pizza_quantity']
#             cart.drink_quantity = form.cleaned_data['drink_quantity']
#             cart.combo_quantity = form.cleaned_data['combo_quantity']
#             cart.save()

#             # Add selected pizzas, drinks, and combos to the ManyToMany fields
#             cart.pizza.set(form.cleaned_data['pizza'])
#             cart.drink.set(form.cleaned_data['drink'])
#             cart.combo.set(form.cleaned_data['combo'])

#             # Redirect to the success page or do something else
#             return redirect('menu_page')
#         else:
#             # Form is not valid, handle the error
#             logger.debug(form)
#             logger.error("Invalid form data: %s", form.errors)
#     else:
#         form = CartForm()

#     return render(request, 'product/menuPage.html', {'form': form})


# def clearCar(request):
#     del request.session['cart']
#     return redirect('cart_cleared')
# def product(request):
#     return HttpResponse('Hello World!')


# def yname(request, name):
#     return render(request, 'name/yname.html', {'namehtml':name})