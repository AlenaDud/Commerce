from django import forms
from .models import Listing, Comments, Bid, Watchlist


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['is_active', 'date_of_create', 'user', 'winner']
        labels = {'name': 'Title',
                  'detail': 'Description',
                  'start_price': 'Starting price in USD',
                  'photo': 'URL of image',
                  'category': 'Category'}


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['detail']


class BidForms(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['cost']
        widgets = {
            'cost': forms.TextInput(attrs={'placeholder': 'Bid'})
        }
