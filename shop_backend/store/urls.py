from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import ProductViewSet, CategoryViewSet, CartView, AddToCartView, UpdateCartItemView, cart_html_view

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='cart-add'),
    path('cart/update/<int:product_id>/', views.cart_item_update, name='cart-item-update'),
    path('auth/', views.auth_view, name='auth'),
    path('category/<int:cat_id>/', views.category_filter, name='category'),
    path('search/', views.search_view, name='search'),

]
