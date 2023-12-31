from django.urls import path
from . import views

urlpatterns = [
    # path('', views.getAllProduct),
    path('', views.MainView.as_view(), name="main_page"),
    path('menu/', views.MenuView.as_view(), name="menu_page"),
    path('cart/', views.ClosedCartView.as_view(), name="cart_page"),
    path('order/', views.OrderView.as_view(), name="order_page"),
    path('order/<int:orderid>/', views.OrderViewDetail.as_view(), name="order_detail_page"),
    # path('user/', views.CartView.as_view(), name="user_page"),
    # path('clearCar/', views.clearCar, name='clear_cart'),
    # path('yname/<str:name>', views.yname, name='name-url')
]
