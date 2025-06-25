from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, CartItem
from rest_framework import viewsets, generics
from django.shortcuts import render, redirect
from .models import Product, Cart
from .filters import ProductFilter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter 
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate
from .serializers import ProductSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request': self.request}

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(['GET'])
def product_search_api(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=q)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_view(request):
    q = request.query_params.get('q', '')
    products = Product.objects.filter(title__icontains=q)
    serialized = ProductSerializer(products, many=True, context={'request': request})
    return Response(serialized.data)


@api_view(['GET'])
def filter_options_api(request):
    from .models import COLOR_CHOICES, Size, Category

    return Response({
        "colors": COLOR_CHOICES,
        "sizes": [ {"slug": s.slug, "name": s.name} for s in Size.objects.all() ],
        "categories": [ {"id": c.id, "name": c.name} for c in Category.objects.all() ]
    })


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        
        # Проверяем, есть ли уже такой товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Если товар уже есть - увеличиваем количество
            cart_item.quantity += quantity
            cart_item.save()


class UpdateCartItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


# def cart_html_view(request):
#     if not request.user.is_authenticated:
#         return redirect('/admin/login/?next=/cart/')
#
#     cart, _ = Cart.objects.get_or_create(user=request.user)
#
#     if request.method == 'POST':
#         if 'product_id' in request.POST:
#             from .models import CartItem, Product
#             product = Product.objects.get(id=request.POST['product_id'])
#             quantity = int(request.POST.get('quantity', 1))
#             CartItem.objects.create(cart=cart, product=product, quantity=quantity)
#
#         elif 'quantity' in request.POST:
#             item_id = request.path.split('/')[-2]
#             try:
#                 item = cart.items.get(id=item_id)
#                 if 'delete' in request.GET:
#                     item.delete()
#                 else:
#                     item.quantity = int(request.POST['quantity'])
#                     item.save()
#             except:
#                 pass
#
#         return redirect('/cart/')
#
#     return render(request, 'cart.html', {'cart': cart})


@api_view(['GET'])
def home_view(request):
    products   = Product.objects.all()
    categories = Category.objects.all()

    products_data   = ProductSerializer(products, many=True, context={'request': request}).data
    categories_data = CategorySerializer(categories, many=True, context={'request': request}).data

    return Response({
        'products':   products_data,
        'categories': categories_data,
    })


@api_view(['GET'])
def product_detail_api(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product , context = {'request':request})
    return Response(serializer.data)

@api_view(['GET'])
def category_filter_api(request, cat_id):
    products   = Product.objects.filter(category_id=cat_id)
    categories = Category.objects.all()
    return Response({
        'products':   ProductSerializer(products,   many=True, context={'request': request}).data,
        'categories': CategorySerializer(categories, many=True, context={'request': request}).data,
    })


# @api_view(['GET'])
# def cart_api(request):
#     cart = request.session.get('cart', {})
#     products = Product.objects.filter(id__in=cart.keys())
#     cart_items = [
#         {
#             'product': ProductSerializer(product, context={'request': request}).data,
#             'quantity': cart[str(product.id)],
#             'total':    cart[str(product.id)] * product.price
#         }
#         for product in products
#     ]
#     return Response({'cart_items': cart_items})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += 1
        else:
            cart[str(product_id)] = 1

        request.session['cart'] = cart
        return redirect('cart')
    return redirect('home')


def cart_item_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
    return redirect('cart')


@api_view(['POST'])
@permission_classes([AllowAny])
def auth_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid credentials'}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    })



