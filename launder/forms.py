from django.forms import ModelForm
from models import (
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
)


class WashFoldOrderForm(ModelForm):
    class Meta:
        model = WashFoldOrder
        exclude = ('date')

class DryCleaningForm(ModelForm):
    class Meta:
        model = DryCleaning
        exclude = ('date')

class LaundryShirtsOrderForm(ModelForm):
    class Meta:
        model = LaundryShirtsOrder
        exclude = ('date', 'shirts_price')