from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique= True , null= True , blank= True)

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

class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)      
    slug = models.SlugField(max_length=10, unique=True, null= True, blank=True)      

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to='products/main/', null=True, blank=True)
    available = models.BooleanField(default=True)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    sizes = models.ManyToManyField(Size, related_name='products', blank=True)
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',    # чтобы получить product.images.all()
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/gallery/')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

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
