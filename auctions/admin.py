from django.contrib import admin
from .models import Listing, Comments, Bid, Watchlist, Category


# Register your models here.


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_editable = ['detail', 'start_price', 'is_active',
                     'photo', 'user', 'category', 'winner']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_editable = ['listing', 'detail']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_editable = ['listing', 'cost']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = '__all__'
    list_editable = ['listing']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = '__all__'
    pass
