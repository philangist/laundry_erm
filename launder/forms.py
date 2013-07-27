from django.forms import ModelForm
from models import WashFoldOrder, DryCleaning, LaundryShirtsOrder


class WashFoldOrderForm(ModelForm):
	class Meta:
		model = WashFoldOrder
		fields = ['first_name', 'last_name', 'phone_number', 'address', 'total_cost', 'payment_method', 'payment_finalized']

class DryCleaningForm(ModelForm):
	class Meta:
		model = DryCleaning
		fields = ['first_name', 'last_name', 'phone_number', 'address', 'total_cost', 'payment_method', 'payment_finalized']

class LaundryShirtsOrderForm(ModelForm):
	class Meta:
		model = LaundryShirtsOrder
		fields = ['first_name', 'last_name', 'phone_number', 'address', 'total_cost', 'payment_method', 'payment_finalized']