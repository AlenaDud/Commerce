from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=60)


class Listing(models.Model):
    name = models.CharField(max_length=60)
    detail = models.TextField(blank=True)
    start_price = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    is_active = models.BooleanField(default=True)
    date_of_create = models.DateField(auto_now=True)
    photo = models.ImageField(upload_to='listings/%Y/%m/%d/',
                              blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='win_user')


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=19, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    detail = models.TextField()


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


