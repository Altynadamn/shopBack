from rest_framework import serializers
from .models import Product, Category, CartItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']


# class FavoriteItemSerializer(serializers.ModelSerializer):
#     propcache = ProductSerializer(read_only=True)
#     product_id = serializers.PrimaryKeyRelatedField(
#         queryset=Product.object.all(), source='product', write_only=True)
#
#     class Meta:
#         model = FavoriteItem
#         fields = ['id', 'user', 'created_at', 'items']
#
#
# class FavoriteSerializer(serializers.ModelSerializer):
#     items = FavoriteItemSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Favorites
#         fields = ['id', 'user', 'created_at', 'items']
#         read_only_fields = ['user', 'created_at']
