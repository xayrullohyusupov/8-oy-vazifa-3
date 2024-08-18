from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import LogoutView, RegisterView,CartView, AddProductToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='get_or_create_cart'),
    path('add-product/', AddProductToCartView.as_view(), name='add_product_to_cart'),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view(), name='api_token_logout'),
    path('register/', RegisterView.as_view(), name='api_register')
]
