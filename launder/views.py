import json
import logger_factory

from itertools import chain
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import (
    ListView,
    DetailView,
)

from django.views.generic.edit import (
    CreateView,
    UpdateView,
    FormView,
)

from launder.forms import (
    WashFoldOrderForm,
    DryCleaningForm,
    LaundryShirtsOrderForm,
    ProductForm,
    UserForm,
)

from launder.models import (
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
    DailyOperations,
    Product,
)

logger = logger_factory.logger_factory('views')


def _filter_customers_by_phone_number(phone_number):
    shirts_qs = list(LaundryShirtsOrder.objects.filter(phone_number=phone_number))
    wash_fold_qs = WashFoldOrder.objects.filter(phone_number=phone_number)
    dry_cleaning_qs = DryCleaning.objects.filter(phone_number=phone_number)
    concatenated_qs = shirts_qs
    concatenated_qs.extend(wash_fold_qs)
    concatenated_qs.extend(dry_cleaning_qs)
    return concatenated_qs


@csrf_exempt
def get_customer_contact_info(request):
    response_content = None
    logger.debug('request: %s', request)
    request_body = json.loads(request.raw_post_data)
    logger.debug('request_body: %s', request_body)

    try:
        phone_number = request_body.get('phone_number')
    except TypeError, KeyError:
        logger.warning('Invalid phone number used for autocomplete',
                    exc_info=True)
        response_content = None
    finally:
        if phone_number:
            customers = list(set([
                '%s&-&%s' % (customer.first_name, customer.last_name)
                for customer in _filter_customers_by_phone_number(phone_number)
            ]))

            logger.debug('Customers: %s', customers)
            response_content = json.dumps(customers)

        response = HttpResponse(
            response_content, content_type="application/json")

    return response


class NavBarMixin(object):
    def get_context_data(self, **kwargs):
        context = super(NavBarMixin, self).get_context_data(**kwargs)
        context.update({'active_tab' : self.get_active_tab()})
        return context

    def get_active_tab(self):
        try:
            active_tab = self.active_tab
        except:
            active_tab = 'home'
        return active_tab


class LaundryIndex(NavBarMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'daily_orders_list'
    paginate_by = 5

    def get_queryset(self):
        wash_fold_set = WashFoldOrder.objects.filter(payment_finalized=False)
        dry_clean_set = DryCleaning.objects.filter(payment_finalized=False)
        shirts_set = LaundryShirtsOrder.objects.filter(payment_finalized=False)
        queryset =  list(chain(
            wash_fold_set,
            dry_clean_set,
            shirts_set,
            )
        )
        queryset.sort(key = lambda o: o.date)
        queryset.reverse()
        return queryset


def extract_date_data():
    seen_dates = {}
    def process_order_list(order_list):
        for order in order_list:
            cur_date = order.date.date()
            payment_date = order.payment_date.date()
            if cur_date not in seen_dates:
                seen_dates[cur_date] = [0, 0]
            if payment_date not in seen_dates:
                seen_dates[payment_date] = [0, 0]
            if payment_date != cur_date:
                cur_date = payment_date
            seen_dates[cur_date][0] += 1
            seen_dates[cur_date][1] += order.total_cost
    dry_clean_list = DryCleaning.objects.all().order_by('-date')
    shirts_list = LaundryShirtsOrder.objects.all().order_by('-date')
    wash_fold_list = WashFoldOrder.objects.all().order_by('-date')
    process_order_list(dry_clean_list)
    process_order_list(shirts_list)
    process_order_list(wash_fold_list)
    context_objects_list = []
    for date, date_info in seen_dates.iteritems():
        date_tuple = (date.isoformat(), date_info[0], date_info[1])
        context_objects_list.append(date_tuple)
    context_objects_list.sort()
    context_objects_list.reverse()
    return context_objects_list


class DailyOperationsList(NavBarMixin, ListView):
    template_name = 'launder/daily_ops_dates_list.html'
    context_object_name = 'date_data'
    paginate_by = 5
    active_tab = 'daily_ops'
    queryset = WashFoldOrder.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsList, self).get_context_data(**kwargs)
        context['date_data'] = extract_date_data()
        return context


class DailyOperationsDateView(NavBarMixin, ListView):
    context_object_name = 'orders_list'
    template_name = 'launder/daily_ops_date.html'
    active_tab = 'daily_ops'

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsDateView, self).get_context_data(**kwargs)
        context['current_date'] = '%s-%s-%s' % (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
        )
        return context

    def get_queryset(self):
        self.date_string = '%s-%s-%s' % (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
        )
        wash_fold_set = WashFoldOrder.objects.filter(date__startswith=self.date_string)
        dry_clean_set = DryCleaning.objects.filter(date__startswith=self.date_string)
        shirts_set = LaundryShirtsOrder.objects.filter(date__startswith=self.date_string)
        queryset =  list(chain(
            wash_fold_set,
            dry_clean_set,
            shirts_set,
            )
        )
        queryset.sort(key = lambda o: o.date)
        queryset.reverse()
        return queryset


def extract_products_date_data():
    from launder.models import Product
    seen_dates = {}
    all_dates = list(set(
        [product.date.date() for product in Product.objects.all()]
    ))
    for each_date in all_dates:
        each_date = str(each_date)
        year, month, day = each_date.split('-')
        filter_kwargs = {
            'date__year': year,
            'date__month': month,
            'date__day': day,
        }
        total_sales = len(Product.objects.filter(**filter_kwargs))
        total_revenue = sum([
            each_product.price for each_product in Product.objects.all().filter(**filter_kwargs)
        ])
        seen_dates[each_date] = (total_sales, total_revenue)
    context_objects_list = []
    for date, date_info in seen_dates.iteritems():
        date_tuple = (date, date_info[0], date_info[1])
        context_objects_list.append(date_tuple)
    context_objects_list.sort()
    context_objects_list.reverse()
    return context_objects_list


class DailyOperationsProductsList(ListView):
    template_name = 'launder/daily_ops_dates_list.html'
    active_tab = 'product'
    context_object_name = 'date_data'
    paginate_by = 5
    queryset = Product.objects.all()
    model = Product

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsProductsList, self).get_context_data(**kwargs)
        context['date_data'] = extract_products_date_data()
        context['product_date_data'] = True
        return context


class DailyOperationsProductsDateList(ListView):
    template_name = 'launder/daily_ops_product_dates_list.html'
    context_object_name = 'products'
    paginate_by = 5
    active_tab = 'product'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsProductsDateList, self).get_context_data(**kwargs)
        context['current_date'] = '%s-%s-%s' % (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
        )
        return context

    def get_queryset(self):
        self.date_string = '%s-%s-%s' % (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
        )
        queryset = Products.objects.filter(date=self.date_string)
        queryset.sort(key = lambda o: o.date)
        queryset.reverse()
        return queryset


class DailyOperationsArchive(NavBarMixin, ListView):
    template_name = 'archive.html'
    context_object_name = 'daily_orders_list'
    active_tab = 'archive'
    wash_fold_set = WashFoldOrder.objects.filter(payment_finalized=True)
    dry_clean_set = DryCleaning.objects.filter(payment_finalized=True)
    shirts_set = LaundryShirtsOrder.objects.filter(payment_finalized=True)
    queryset =  list(chain(
        wash_fold_set,
        dry_clean_set,
        shirts_set,
        )
    )
    queryset.sort(key = lambda o: o.date)
    queryset.reverse()
    paginate_by = 5


class DailyOperationsDryCleaningArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'dry_cleaning'
    queryset = DryCleaning.objects.all().filter(payment_finalized=True).order_by('-id')
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsDryCleaningArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'dry_cleaning'
        return context


class DailyOperationsLaundryShirtsArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'shirts'
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True).order_by('-id')
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsLaundryShirtsArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'shirts'
        return context


class DailyOperationsWashFoldArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'wash_fold'
    queryset = WashFoldOrder.objects.all().filter(payment_finalized=True).order_by('-id')
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsWashFoldArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'wash_fold'
        return context


class WashFoldCreate(CreateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'


class WashFoldUpdate(UpdateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'


class WashFoldList(NavBarMixin, ListView):
    active_tab = 'wash_fold'
    queryset= WashFoldOrder.objects.all().filter(payment_finalized=False).order_by('-id')
    template_name = 'launder/wash_fold_list.html'
    paginate_by = 5


class WashFoldDetail(DetailView):
    context_object_name = 'wash_fold_order'
    template_name = 'launder/wash_fold_detail.html'
    model = WashFoldOrder


class DryCleaningCreate(CreateView):
    model = DryCleaning
    form_class = DryCleaningForm
    template_name = 'launder/dry_cleaning_form.html'


class DryCleaningUpdate(UpdateView):
    model = DryCleaning
    form_class = DryCleaningForm
    template_name = 'launder/dry_cleaning_form.html'


class DryCleaningList(NavBarMixin, ListView):
    active_tab = 'dry_cleaning'
    queryset= DryCleaning.objects.all().filter(payment_finalized=False).order_by('-id')
    template_name = 'launder/dry_cleaning_list.html'
    paginate_by = 5


class DryCleaningDetail(DetailView):
    context_object_name = 'dry_cleaning_order'
    template_name = 'launder/dry_cleaning_detail.html'
    model = DryCleaning


class LaundryShirtsOrderCreate(CreateView):
    model = LaundryShirtsOrder
    form_class = LaundryShirtsOrderForm
    template_name = 'launder/shirts_form.html'


class LaundryShirtsOrderUpdate(UpdateView):
    model = LaundryShirtsOrder
    form_class = LaundryShirtsOrderForm
    template_name = 'launder/shirts_form.html'


class LaundryShirtsOrderList(NavBarMixin, ListView):
    active_tab = 'shirts'
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=False).order_by('-id')
    template_name = 'launder/shirts_list.html'
    paginate_by = 5


class LaundryShirtsOrderDetail(DetailView):
    context_object_name = 'shirts_order'
    template_name = 'launder/shirts_detail.html'
    model = LaundryShirtsOrder


class ProductCreate(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'launder/product_form.html'


class ProductUpdate(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'launder/product_form.html'


class ProductList(NavBarMixin, ListView):
    model = Product
    queryset = list(set(product.name for product in Product.objects.all()))
    template_name = 'launder/product_list.html'
    paginate_by = 5
    active_tab = 'products'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        product_names = set([each_product.name for each_product in Product.objects.all()])
        context['products'] = set([
            Product.objects.filter(name=name)[:1].get() for name in product_names])
        return context


class ProductDetail(DetailView):
    context_object_name = 'product'
    template_name = 'launder/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product_name = kwargs['object'].name
        context['number_sales'] = len(Product.objects.all().filter(name=product_name))
        context['total_revenue'] = sum([
            each_product.price for each_product in Product.objects.all().filter(name=product_name)])
        return context


class CustomerOrdersList(DetailView):
    context_object_name = 'orders_list'
    template_name = 'launder/customer_orders_list.html'
    slug_field = 'customer_name_slug'
    model = WashFoldOrder

    def get_object(self, *args, **kwargs):
        return WashFoldOrder.objects.all()[0]

    def get_context_data(self, *args, **kwargs):
        context = super(CustomerOrdersList, self).get_context_data(**kwargs)
        first_name ,last_name = self.kwargs['customer_name_slug'].split('-')

        filter_kwargs = {
            'first_name': first_name,
            'last_name': last_name,
        }

        wash_fold_set = WashFoldOrder.objects.filter(**filter_kwargs)
        dry_clean_set = DryCleaning.objects.filter(**filter_kwargs)
        shirts_set = LaundryShirtsOrder.objects.filter(**filter_kwargs)
        order_list =  list(chain(
            wash_fold_set,
            dry_clean_set,
            shirts_set,
            )
        )
        order_list.sort(key = lambda o: o.date)
        context['orders_list'] = order_list
        context['first_name'] = first_name.capitalize()
        context['last_name'] = last_name.capitalize()
        return context


class UserCreate(FormView):
    model = User
    form_class = UserForm
    template_name = 'registration/add_user.html'
    success_url = '/'

    def form_valid(self, form):
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.is_staff = True
        user.save()
        return super(UserCreate, self).form_valid(form)

class PrintOrder(ListView):
    model = WashFoldOrder
    context_object_name = 'order'
    template_name = 'launder/print_order.html'

    def get_context_data(self, **kwargs):
        logger.info('args: {}'.format(str(self.args)))
        context = super(PrintOrder, self).get_context_data(**kwargs)
        if self.args[0] == 'dry_cleaning':
            order = DryCleaning
        elif self.args[0] == 'wash_fold':
            order = WashFoldOrder
        else:
            order = LaundryShirtsOrder

        try:
            order = order.objects.get(pk=self.args[1])
        except:
            order = None
        else:
            context['order_first_name'] = order.first_name
            context['order_last_name'] = order.last_name
            context['order_type'] = order.order_type
            context['order_date'] = order.date
            context['order_total_cost'] = order.total_cost
            context['order_payment_finalized'] = order.payment_finalized
            context['order_comments'] = order.comments
        return context
