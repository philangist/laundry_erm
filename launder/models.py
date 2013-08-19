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
    address = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(default=datetime.datetime.today().date)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField(default=False)
    payment_date = models.DateTimeField(default=datetime.datetime.today)
    comments = models.TextField(default='', blank=True)

    def __unicode__(self):
        return '%s %s - $%s - %s' % (self.first_name, self.last_name, self.total_cost, self.date.date())

    def get_absolute_url(self):
        return reverse('wash_fold_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Wash and Fold'

    @property
    def order_type_slug(self):
        return 'wash_fold'

class DryCleaning(models.Model):

    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CREDIT', 'Credit'),
        ('CHECK', 'Check')
    )

    GARMENT_OPTIONS = (
        ('TROUSERS', 'Trousers'),
        ('M SUITS', 'Men\'s Suits'),
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
    address = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(default=datetime.datetime.today().date)
    garment_type = models.CharField(max_length=12, choices=GARMENT_OPTIONS)
    garment_amount = models.IntegerField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField()
    payment_date = models.DateTimeField(default=datetime.datetime.today)

    def __unicode__(self):
        return '%s %s - $%s - %s' % (self.first_name, self.last_name, self.total_cost, self.date.date())

    def get_absolute_url(self):
        return reverse('dry_cleaning_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Dry Cleaning'

    @property
    def order_type_slug(self):
        return 'dry_cleaning'



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
    address = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(default=datetime.datetime.today().date)
    shirts_amount = models.IntegerField()
    shirts_price = models.DecimalField(max_digits=8, decimal_places=2)
    starched = models.BooleanField()
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField()
    payment_date = models.DateTimeField(default=datetime.datetime.today)

    def __unicode__(self):
        return '%s %s - $%s - %s' % (self.first_name, self.last_name, self.total_cost, self.date.date())
    
    def get_absolute_url(self):
        return reverse('shirts_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Shirt'

    @property
    def order_type_slug(self):
        return 'shirts'

class DailyOperations(models.Model):
    date = models.DateTimeField(default=datetime.datetime.today)

    def __unicode__(self):
        return '%s' % str(self.date)