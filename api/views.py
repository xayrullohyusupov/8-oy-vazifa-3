from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics,status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from Goods.models import Cart, Product, CartProduct
from .serializers import UserRegistrationSerializer,CartSerializer,ProductSerializer
from rest_framework.decorators import api_view


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logged out successfully"}, status=204)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        print(token.key)
        return Response({"token": token.key}, status=201)
        

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(author=request.user, is_active=True)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddProductToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_code = request.data.get('product_code')
        try:
            product = Product.objects.get(generate_code=product_code)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        cart, _ = Cart.objects.get_or_create(author=request.user, is_active=True)
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_product.quantity += 1
            cart_product.save()

        return Response({"message": f"Product {product_code} added to cart"})