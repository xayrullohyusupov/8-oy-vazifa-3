from django.db import models
from django.contrib.auth.models import User
from random import sample
import string

class GenereteCode(models.Model):
    generate_code = models.CharField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.generate_code:
            self.generate_code = "".join(sample(string.ascii_letters, 20))
        super(GenereteCode, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Banner(GenereteCode):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(GenereteCode):
    name = models.CharField(max_length=255)
    generate_code = models.CharField(max_length=255, blank=True, unique=True)
    title = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

class Product(GenereteCode):
    name:str = models.CharField(max_length=255)
    quantity:int = models.PositiveIntegerField(default=1)
    price:float = models.DecimalField(max_digits=8, decimal_places=2)
    category:Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description:str = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    
class ProductEnter(GenereteCode):
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    old_quantity = models.IntegerField(blank=True)
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if not self.generate_code:
            self.old_quantity = self.product.quantity
            self.product.quantity += self.quantity
        else:
            self.product.quantity -= ProductEnter.objects.get(generate_code=self.generate_code).quantity
            self.product.quantity += self.quantity
        self.product.save()
        super(ProductEnter, self).save(*args, **kwargs)

class ProductImg(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product-img')

    def __str__(self):
        return self.product.name

class Cart(GenereteCode):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    shopping_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.author.username

class CartProduct(GenereteCode):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

class Order(GenereteCode):
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=255)
    status = models.SmallIntegerField(
        choices=(
            (1, 'Tayyorlanmoqda'),
            (2, 'Yo`lda'),
            (3, 'Yetib borgan'),
            (4, 'Qabul qilingan'),
            (5, 'Qaytarilgan'),
        )
    )

    def __str__(self):
        return self.full_name


class NavbarInfo(GenereteCode):
    name = models.CharField(max_length = 25)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class FooterInfo(GenereteCode): 
    name = models.CharField(max_length = 25)
    phone = models.CharField(max_length=15, blank=True, null=True)
    title = models.TextField(max_length=35)

    def __str__(self):
        return self.name


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}, {self.product.name}"