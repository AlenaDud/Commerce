from django.contrib import admin
from .models import Listing, Comments, Bid, Watchlist, Category, User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


class PriceFilter(admin.SimpleListFilter):
    title = 'Start price filter'
    parameter_name = 'start_price'

    def lookups(self, request, model_admin):
        return [
            ('<30', 'Cheap'),
            ('30-100', 'Medium'),
            ('>100', 'Expensive'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<30':
            return queryset.filter(start_price__lte=30)
        if self.value() == '30-100':
            return queryset.filter(start_price__gt=30, start_price__lte=100)
        if self.value() == '>100':
            return queryset.filter(start_price__gt=100)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['name', 'detail', 'start_price', 'is_active',
                    'photo', 'user', 'category', 'winner']
    list_editable = ['detail', 'start_price', 'is_active',
                     'photo', 'user', 'category', 'winner']
    list_filter = ['is_active', 'category', PriceFilter]
    search_fields = ['name']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'detail']
    list_editable = ['listing', 'detail']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'cost']
    list_editable = ['listing', 'cost']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing']
    list_editable = ['listing']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    pass
