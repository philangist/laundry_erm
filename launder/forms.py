from django.forms import ModelForm
from django.contrib.auth.models import User

from models import (
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
    Product,
)


class WashFoldOrderForm(ModelForm):
    class Meta:
        model = WashFoldOrder
        exclude = ('date', 'payment_date')


class DryCleaningForm(ModelForm):
    class Meta:
        model = DryCleaning
        exclude = ('date' 'payment_date')


class LaundryShirtsOrderForm(ModelForm):
    class Meta:
        model = LaundryShirtsOrder
        exclude = ('date', 'shirts_price', 'payment_date')


class ProductForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('date')


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'is_staff',
        )
