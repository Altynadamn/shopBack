from rest_framework import serializers
from .models import Product, Category, CartItem, Cart, ProductImage, Size


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name', 'slug']

class ProductImageSerializer(serializers.ModelSerializer):
    # use_url=True и контекст request дадут абсолютный URL
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(use_url=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    category   = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'category',
            'main_image', 'images', 'available', 'color' , 'sizes'
        ]


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
        fields = ['id', 'user', 'date_added', 'items']
        read_only_fields = ['user', 'date_added']


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
