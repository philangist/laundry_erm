import datetime
from django.core.urlresolvers import reverse
from django.db import models

class WashFoldOrder(models.Model):

    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit'),
        ('CHECK', 'Check')
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.CharField(max_length=50, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField(default=False)
    payment_date = models.DateTimeField(default=datetime.date.today)
    comments = models.TextField(default='')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('wash_fold_detail', kwargs={'wash_fold_order': self.pk})

class DryCleaning(models.Model):

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
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.CharField(max_length=50, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    garment_type = models.TextField(max_length=12, choices=GARMENT_OPTIONS)
    garment_amount = models.IntegerField()
    total_cost = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField()
    payment_date = models.DateTimeField(default=datetime.date.today)

class LaundryShirtsOrder(models.Model):

    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit'),
        ('CHECK', 'Check')
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.CharField(max_length=50, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    shirts_amount = models.IntegerField()
    shirts_price = models.DecimalField(max_digits=5, decimal_places=2)
    starched = models.BooleanField()
    total_cost = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField()
    payment_date = models.DateTimeField(default=datetime.date.today)

class DailyOperationsList(models.Model):

    date = models.DateTimeField(datetime.datetime.today())