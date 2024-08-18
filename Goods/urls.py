from django.urls import path, include
from django.contrib.auth import views as auth_views
from Goods import views
from . import views


urlpatterns = [
    path('', views.main, name='index'),
    path('shop/', views.shop, name='shop'),
    path('shop_list/',views.shop_list, name='shop_list'),
    path('shop_detail/',views.shop_detail, name='shop_detail'), 
    path('authentication/', include('Goods.authentication.urls')),
    path('back-office/', include('Goods.back-office.urls')),
    path('user/', include('Goods.user.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
]