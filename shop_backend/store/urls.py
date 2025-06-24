from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import filter_options_api

from . import views
from .views import (
    ProductViewSet, CategoryViewSet,
    CartView, AddToCartView, UpdateCartItemView,
    search_view, home_view, product_detail_api,
    category_filter_api, cart_api, auth_api
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/update/<int:product_id>/', UpdateCartItemView.as_view(), name='cart-item-update'),

    path('search/', views.search_view, name='search'),
    path('home/',               home_view,          name='home'),
    path('category/<int:cat_id>/', views.category_filter_api, name='category'),
    path('cart-json/',          cart_api,           name='cart-json'),
    path('filter-options/', filter_options_api, name='filter_options'),

]
