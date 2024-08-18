from django.shortcuts import render, redirect
from Goods import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


def myCart(request):
    cart = models.Cart.objects.get(author=request.user, is_active=True)
    context = {'cart': cart}
    return render(request, 'cart.html', context)


def addProductToCart(request):
    code = request.GET['code']
    quantity = int(request.GET['quantity'])
    product = models.Product.objects.get(generate_code=code)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    try:
        cart_product = models.CartProduct.objects.get(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()
    except models.CartProduct.DoesNotExist:
        models.CartProduct.objects.create(
            product=product, 
            cart=cart,
            quantity=quantity
        )
    return redirect('my_cart')


def substractProductFromCart(request):
    code = request.GET['code']
    quantity = int(request.GET['quantity'])  # convert to int
    product = models.Product.objects.get(generate_code=code)
    cart_product = models.CartProduct.objects.get(cart__author=request.user, cart__is_active=True, product=product)
    cart_product.quantity -= quantity
    if cart_product.quantity <= 0:
        cart_product.delete()
    else:
        cart_product.save()
    return redirect('my_cart')


def deleteProductCart(request):
    code = request.GET['code']
    product = models.Product.objects.get(generate_code=code)
    cart_product = models.CartProduct.objects.get(cart__author=request.user, cart__is_active=True, product=product)
    cart_product.delete()
    return redirect('my_cart')


def CreateOrder(request):
    cart = models.Cart.objects.get(generate_code=request.GET['generate_code'], author=request.user)
    cart_products = models.CartProduct.objects.filter(cart=cart)

    done_products = []

    for cart_product in cart_products:
        if cart_product.quantity <= cart_product.product.quantity:
            cart_product.product.quantity -= cart_product.quantity
            cart_product.product.save()
            done_products.append(cart_product)
        else:
            for product in done_products:
                product.product.quantity += product.quantity
                product.product.save()
            raise ValueError('Qoldiqda kamchilik')

    models.Order.objects.create(
        cart=cart,
        full_name=f"{request.user.first_name}, {request.user.last_name}",
        email=request.user.email,
        phone=request.GET['phone'],
        address=request.GET['address'],
        status=1
    )
    cart.is_active = False
    cart.save()
    
    return redirect('my_cart')



@login_required
def wishList(request):
    wish_list = models.WishList.objects.filter(user=request.user)
    context = {'wish_list': wish_list}
    return render(request, 'wishlist.html', context)

@login_required
def addOrDeleteWishList(request, code):
    product = get_object_or_404(models.Product, generate_code=code)
    data, is_create = models.WishList.objects.get_or_create(product=product, user=request.user)
    if not is_create:
        data.delete()
    return redirect('wishlist')

def userSearch(request):
    q = request.GET.get('q')
    if q:
        result = models.Product.objects.filter(name__icontains=q)
        return render(request, 'user/query.html', {'result': result})
    return redirect('/')

"""

Product.objects.filter(
    created_at:date = date,
    created_at:date__gt = date,
    created_at:date__gte = date,
    created_at:date__lt = date,
    created_at:date__lte = date,
)

Product.objects.filter(
    created_at:time = time
)

Product.objects.filter(
    created_at:date_time = date_time
)

Product.objects.filter(
    created_at:date_time__year = 2024,
    region_name__icontains = 'a'
)

# 12, 15, 15, 10
# Yan, Fev, Mar, Apr, May, Iy, ... Dec
[10,11,12,13,15,16,17,123,432,123]
[Yan, Fev, Mar, Apr, May, Iy, iyul, avg, sen, okt, Dec]

product = Product.objects.all()
paginator = Paginator(product, per_page=3)
product = [1,2,3,4,5,6,7,8,9,10]
paginator = [[1,2,3]]
paginator.object_list -> 4

"""