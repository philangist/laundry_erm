import datetime
from django.core.urlresolvers import reverse
from django.db import models


class Order(models.Model):
    """
    Base class for all orders.

    """

    class Meta:
        abstract = True

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
    date = models.DateTimeField(default=datetime.datetime.today)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=6, choices=PAYMENT_METHODS)
    payment_finalized = models.BooleanField()
    payment_date = models.DateTimeField(default=datetime.datetime.today)
    comments = models.TextField(default='', blank=True)
    staff_comments = models.TextField(default='', blank=True)

    def save(self):
        """
        Get or create a Transaction object for this order, and update it with
        payment status and cost

        """

        super(Order, self).save()

        try:
            transaction = Transaction.objects.get(
                transaction_type=self.order_type,
                transaction_id=self.id
            )
        except Transaction.DoesNotExist:
            transaction = Transaction.objects.create(
                transaction_id=self.id,
                transaction_type=self.order_type,
                date_opened=self.date,
                total_cost=self.total_cost
            )

        transaction.total_cost = self.total_cost
        transaction.payment_finalized = self.payment_finalized
        transaction.payment_date = self.payment_date
        transaction.save()


class WashFoldOrder(Order):

    weight = models.IntegerField(default=0)
    num_comforters = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return '{} {} - ${} - {}'.format(self.first_name, self.last_name, self.total_cost, self.date.date())

    def get_absolute_url(self):
        return reverse('wash_fold_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Wash and Fold'

    @property
    def order_type_slug(self):
        return 'wash_fold'


class DryCleaning(Order):

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

    garment_type = models.CharField(max_length=12, choices=GARMENT_OPTIONS)
    garment_amount = models.IntegerField()

    def __unicode__(self):
        return '{} {} - ${} - {}'.format(self.first_name, self.last_name, self.total_cost, self.date.date())

    def get_absolute_url(self):
        return reverse('dry_cleaning_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Dry Cleaning'

    @property
    def order_type_slug(self):
        return 'dry_cleaning'


class LaundryShirtsOrder(Order):

    shirts_amount = models.IntegerField()
    shirts_price = models.DecimalField(default=1.75, max_digits=8, decimal_places=2)
    starched = models.BooleanField()

    def __unicode__(self):
        return '{} {} - ${} - {}'.format(self.first_name, self.last_name, self.total_cost, self.date.date())

    def get_absolute_url(self):
        return reverse('shirts_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Shirt'

    @property
    def order_type_slug(self):
        return 'shirts'


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField(default=datetime.datetime.today)

    def __unicode__(self):
        return '{}: {} - ${}'.format(self.__class__.__name__, self.name, self.date)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    @property
    def order_type(self):
        return 'Product'

    def save(self):
        """
        Get or create a Transaction object for this sale

        """

        super(Product, self).save()

        try:
            transaction = Transaction.objects.get(
                transaction_type=self.order_type,
                transaction_id=self.id
            )
        except Transaction.DoesNotExist:
            transaction = Transaction.objects.create(
                transaction_id=self.id,
                transaction_type=self.order_type,
                date_opened=self.date,
                total_cost=self.price
            )

        transaction.total_cost = self.price
        transaction.payment_finalized = True
        transaction.payment_date = self.date
        transaction.save()

class Transaction(models.Model):
    """
    Represents an individual transaction on a particular date by
    a particular customer. Defaults to 'Two Boys' as customer for
    sales that don't directly involve storing the customer, i.e
    buying laundry detergent or fabric softener

    """

    class Meta:
        unique_together = (('transaction_type', 'transaction_id'))

    TRANSACTION_TYPES = (
        ('DRY_CLEANING', 'Dry Cleaning'),
        ('WASH_FOLD', 'Wash and Fold'),
        ('SHIRT', 'Shirt'),
        ('PRODUCT', 'Product'),
    )

    id = models.AutoField(primary_key=True)
    transaction_id = models.IntegerField(default=0)
    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES)
    date_opened = models.DateTimeField(
        blank=False, default=datetime.datetime.now)
    payment_date = models.DateTimeField(
        blank=True, default=datetime.datetime.now)
    total_cost = models.DecimalField(
        blank=True, max_digits=8, decimal_places=2)
    payment_finalized = models.BooleanField()

    def __unicode__(self):
        return '{} - {} -{}' .format(
            self.transaction_type,
            self.total_cost,
            self.date_opened
        )


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=15, blank=False)
    address = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return '{} - {} {}'.format(
            self.__class__.__name__,
            self.first_name,
            self.last_name,
        )

    @property
    def slug(self):
        return 'customers'

    def get_absolute_url(self):
        return reverse(
            'customer_order_list',
            kwargs={'customer_name_slug':
                        '%s-%s' % (self.first_name, self.last_name)}
        )
