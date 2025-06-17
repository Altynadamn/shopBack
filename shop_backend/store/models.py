from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


COLOR_CHOICES = [
    ("black", "Black"),
    ("white", "White"),
    ("red", "Red"),
    ("blue", "Blue"),
    ("green", "Green"),
    ("yellow", "Yellow"),
]


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    available = models.BooleanField(default=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} s cart'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

#
# class Favorites(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} s favorites'
#
#
# class FavoriteItem(models.Model):
#     liked = models.ForeignKey(Favorites, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"
