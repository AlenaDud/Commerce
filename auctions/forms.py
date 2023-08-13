from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['is_active', 'date_of_create', 'user', 'winner']
        labels = {'name': 'Title',
                  'detail': 'Description',
                  'start_price': 'Starting price',
                  'photo': 'URL of image',
                  'category': 'Category'}

