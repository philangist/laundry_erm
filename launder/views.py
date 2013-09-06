import json
import logger_factory

from itertools import chain
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)

from launder.forms import (
    WashFoldOrderForm,
    DryCleaningForm,
    LaundryShirtsOrderForm,
)
from launder.models import (
    WashFoldOrder,
    DryCleaning,
    LaundryShirtsOrder,
    DailyOperations,
)
from redis_utils import (
    get_redis_client,
    set_contact_info,
    get_contact_info,
)

redis_client = get_redis_client()
logger = logger_factory.logger_factory('views')


@csrf_exempt
def get_customer_contact_info(request):
    response_data = {}
    logger.debug('request.body %s' % str(request.body))
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            data = None
        if data:
            contact_info = get_contact_info(
                data['first_name'],
                data['last_name'],
                redis_client,
            )
            response_data['result'] = contact_info
        else:
            logger.debug('Data was not converted to JSON')
            response_data['result'] = 'No info found for supplied data'
    else:
        logger.debug('Invalid Method')
        response_data['result'] = 'Invalid Method'
    response_data = json.dumps(response_data)
    logger.debug('response_data %s' % str(response_data))
    response = HttpResponse(response_data, mimetype="application/json")
    logger.debug('response %s' % str(response))
    return response

@csrf_exempt
def set_customer_contact_info(request):
    response_content = {}
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except ValueError:
            data = None
        if data:
            logger.info('set customer info data: %s' % str(data))
            contact_info = set_contact_info(
                data['first_name'],
                data['last_name'],
                [data['phone_number'], data['address']],
                redis_client,
            )
        else:
            response_content['error'] = 'Invalid JSON args'
    else:
        response_content['error'] = 'Invalid Method'
    response_content = json.dumps(response_content)
    logger.info('response_content: %s' % response_content)
    response = HttpResponse(response_content, content_type="application/json")
    logger.info('response: %s' % response.__dict__)
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
        
    def get_queryset(self):
        self.date_string = '%s-%s-%s' % (
            self.kwargs['year'],
            self.kwargs['month'],
            self.kwargs['day'],
        )
        wash_fold_set = WashFoldOrder.objects.filter(date=self.date_string)
        dry_clean_set = DryCleaning.objects.filter(date=self.date_string)
        shirts_set = LaundryShirtsOrder.objects.filter(date=self.date_string)
        queryset =  list(chain(
            wash_fold_set,
            dry_clean_set,
            shirts_set,
            )
        )
        queryset.sort(key = lambda o: o.date)
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
    paginate_by = 5

class DailyOperationsDryCleaningArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'dry_cleaning'
    queryset = DryCleaning.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsDryCleaningArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'dry_cleaning'
        return context

class DailyOperationsLaundryShirtsArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'shirts'
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsLaundryShirtsArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'shirts'
        return context

class DailyOperationsWashFoldArchive(NavBarMixin, ListView):
    date_field = 'date'
    active_tab = 'wash_fold'
    queryset = WashFoldOrder.objects.all().filter(payment_finalized=True)
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
    queryset= WashFoldOrder.objects.all().filter(payment_finalized=False)
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
    queryset= DryCleaning.objects.all().filter(payment_finalized=False)
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
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=False)
    template_name = 'launder/shirts_list.html'
    paginate_by = 5

class LaundryShirtsOrderDetail(DetailView):
    context_object_name = 'shirts_order'
    template_name = 'launder/shirts_detail.html'
    model = LaundryShirtsOrder