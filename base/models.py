from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User info"
        verbose_name_plural = "Users info"


class RacingSeries(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Racing Series"
        verbose_name_plural = "Racing Series"


class Team(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    racing_series = models.ForeignKey(RacingSeries, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['racing_series', 'name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=500)
    seller = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    racing_series = models.ForeignKey(RacingSeries, on_delete=models.CASCADE, blank=True, null=True, related_name='products_by_team')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.product.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)

    def calculate_total(self):
        return sum(item.subtotal() for item in self.items.all())

