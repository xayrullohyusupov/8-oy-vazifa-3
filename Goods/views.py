from django.shortcuts import render,redirect,get_object_or_404
from . import models
from django.contrib.auth.forms import UserCreationForm
from .forms import ProductEnterForm
from .models import ProductEnter


def main(request):
    banners = models.Banner.objects.filter(is_active = True)[:5]
    navbar_info = models.NavbarInfo.objects.get()
    footer_info = models.FooterInfo.objects.get()

    context = {}
    context['banners'] = banners
    context['navbar_info'] = navbar_info
    context['footer_info'] = footer_info

    return render(request, 'index.html',context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/login.html', {'form': form})


def create_product(request):
    if request.method == 'POST':
        form = ProductEnterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductEnterForm()
    return render(request, 'create_product.html', {'form': form})

def product_list(request):
    products = ProductEnter.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(ProductEnter, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def update_product(request, pk):
    product = get_object_or_404(ProductEnter, pk=pk)
    if request.method == 'POST':
        form = ProductEnterForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductEnterForm(instance=product)
    return render(request, 'update_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(ProductEnter, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})

def shop(request):
    return render(request, 'shop.html')

def shop_list(request):
    return render(request, 'shop-list.html')

def shop_detail(request):
    return render(request, 'shop-details.html')