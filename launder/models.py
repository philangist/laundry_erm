from django.db import models

class WashFoldOrder(models.Model):
	"""
	order number(primary key)
	customer's name,
	customer's Phone number
	customer's address
	date the order came in
	amount of laundry
	total_cost based on price list entered on data base.
	payment_method
	payment_finalized
	"""

	PAYMENT_METHODS = (
		('CASH', 'Cash'),
		('CREDIT', 'Credit'),
		('CHECK', 'Check')
	)

	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	address = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now_add=True)
	#amount
	total_cost = models.DecimalField(max_digits=5, decimal_places=2)
	payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
	payment_finalized = models.BooleanField()

class DryCleaningForm(models.Model):

	PAYMENT_METHODS = (
		('CASH', 'Cash'),
		('CREDIT', 'Credit'),
		('CHECK', 'Check')
	)

	GARMENT_OPTIONS = (
		('TROUSERS', 'Trousers'),
		('M SUITS', 'M Suits'),
		('TOP O COAT', 'Top O Coat'),
		('SHIRTS', 'Shirts'),
		('SPORTS COATS', 'Sports Coats'),
		('NECKTIES', 'Neckties - Hats'),
		('SWEATERS', 'Sweaters'),
		('DRESS', 'Dress'),
		('SKIRTS', 'Skirts'),
		('L SUITS', 'L Suits'),
		('BLOUSE', 'Blouse'),
		('TOP 3/4 COAT', 'Top 3/4 Coat'),
		('CAR COAT', 'Car Coat'),
		('SLACKS', 'Slacks')
	)

	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	address = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now_add=True)
	garment_type = models.TextField(max_length=12, choices=GARMENT_OPTIONS)
	garment_amount = models.IntegerField()
	total_cost = models.DecimalField(max_digits=5, decimal_places=2)
	payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
	payment_finalized = models.BooleanField()

class LaundryShirtsOrder(models.Model):
	"""
	order number(primary key)
	customer's name,
	customer's Phone number
	customer's address
	date the order came in
	amount of laundry
	total_cost based on price list entered on data base.
	payment_method
	payment_finalized
	"""

	PAYMENT_METHODS = (
		('CASH', 'Cash'),
		('CREDIT', 'Credit'),
		('CHECK', 'Check')
	)

	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.CharField(max_length=15)
	address = models.CharField(max_length=50)
	date = models.DateTimeField(auto_now_add=True)
	shirts_amount = models.IntegerField()
	shirts_price = models.DecimalField(max_digits=5, decimal_places=2)
	starched = models.BooleanField()
	total_cost = models.DecimalField(max_digits=5, decimal_places=2)
	payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
	payment_finalized = models.BooleanField()
