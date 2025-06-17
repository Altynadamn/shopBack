from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, CartItem
from rest_framework import viewsets, generics
from django.shortcuts import render, redirect
from django_filters import filters
from .models import Product, Cart


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.CharFilter]
    filter_set_fields = ['category', 'in_stock', 'color', 'price']
    search_fields = ['title', 'description']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


def search_view(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=q)
    return render(request, 'home.html', {'products': products, 'categories': Category.objects.all()})


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
        serializer.save(cart=cart)


class UpdateCartItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


def cart_html_view(request):
    if not request.user.is_authenticated:
        return redirect('/admin/login/?next=/cart/')

    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'product_id' in request.POST:
            from .models import CartItem, Product
            product = Product.objects.get(id=request.POST['product_id'])
            quantity = int(request.POST.get('quantity', 1))
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        elif 'quantity' in request.POST:
            item_id = request.path.split('/')[-2]
            try:
                item = cart.items.get(id=item_id)
                if 'delete' in request.GET:
                    item.delete()
                else:
                    item.quantity = int(request.POST['quantity'])
                    item.save()
            except:
                pass

        return redirect('/cart/')

    return render(request, 'cart.html', {'cart': cart})


def home_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'product_detail.html', {'product': product})


def category_filter(request, cat_id):
    products = Product.objects.filter(category_id=cat_id)
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def search_view(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(title__icontains=q)
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': quantity * product.price,
        })

    return render(request, 'cart.html', {'cart_items': cart_items})


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


def auth_view(request):
    if request.method == 'POST':
        from rest_framework_simplejwt.tokens import RefreshToken
        from django.contrib.auth import authenticate

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            request.session['token'] = str(refresh.access_token)
            return redirect('home')
        else:
            return render(request, 'auth.html', {'error': 'Invalid credentials'})
    return render(request, 'auth.html')


