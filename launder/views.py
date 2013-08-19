from datetime import datetime
import datetime as dt
from itertools import chain
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.views.generic.dates import (
    DayArchiveView,
    ArchiveIndexView,
)

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
import logger_factory

logger = logger_factory.logger_factory('views')

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


class DailyOperationsList(ListView):
    template_name = 'launder/daily_ops_dates_list.html'
    context_object_name = 'dates_list'
    wash_fold_set = list([str(order.date.date()) for order in WashFoldOrder.objects.all().order_by('-date')])
    dry_clean_set = list([str(order.date.date()) for order in DryCleaning.objects.all().order_by('-date')])
    shirts_set = list([str(order.date.date()) for order in LaundryShirtsOrder.objects.all().order_by('-date')])
    paginate_by = 5
    queryset =  list(set(list(chain(
                wash_fold_set,
                dry_clean_set,
                shirts_set,
                )
            )
        )
    )

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsList, self).get_context_data(**kwargs)
        context['total_orders'] = len(self.wash_fold_set) + len(self.dry_clean_set) + len(self.shirts_set)
        context['revenue'] = '500'
        return context

class DailyOperationsDateView(ListView):
    context_object_name = 'orders_list'
    template_name = 'launder/daily_ops_date.html'

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
        logger.info('queryset: %s' % str(queryset))
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
    model = DryCleaning

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