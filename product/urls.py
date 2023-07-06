from django.urls import path
from . import views

urlpatterns = [
    # path('', views.getAllProduct),
    path('', views.CartView.as_view(), name='menu_page'),
    # path('clearCar/', views.clearCar, name='clear_cart'),
    # path('yname/<str:name>', views.yname, name='name-url')
]
