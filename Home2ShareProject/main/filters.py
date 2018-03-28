from main.models import House
from django import forms
from django.forms import MultiWidget
import django_filters

class HouseFilter(django_filters.FilterSet):
    country = django_filters.MultipleChoiceFilter(choices=House.COUNTRIES,widget=forms.CheckboxSelectMultiple)
    price_between = django_filters.RangeFilter(name='price')
    class Meta:
        model = House
        fields = {
            'name': ['icontains'],
            'country':['exact'],
            'room_quantity':['exact'],
            'price_between':['price']
        }
