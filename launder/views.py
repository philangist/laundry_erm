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

class DailyOperationsList(NavBarMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'daily_orders_list'
    wash_fold_set = WashFoldOrder.objects.all()
    dry_clean_set = DryCleaning.objects.all()
    shirts_set = LaundryShirtsOrder.objects.all()
    queryset =  list(chain(
        wash_fold_set,
        dry_clean_set,
        shirts_set,
        )
    )
    paginate_by = 5

class DailyOperationsDryCleaningArchive(NavBarMixin, ArchiveIndexView):
    date_field = 'date'
    active_tab = 'dry_cleaning'
    queryset = DryCleaning.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsDryCleaningArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'dry_cleaning'
        return context

class DailyOperationsLaundryShirtsArchive(NavBarMixin, ArchiveIndexView):
    date_field = 'date'
    active_tab = 'shirts'
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DailyOperationsLaundryShirtsArchive, self).get_context_data(**kwargs)
        context['order_type'] = 'shirts'
        return context

class DailyOperationsWashFoldArchive(NavBarMixin, ArchiveIndexView):
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
    queryset= WashFoldOrder.objects.all().filter(payment_finalized=True)
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
    queryset= DryCleaning.objects.all().filter(payment_finalized=True)
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
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/shirts_list.html'
    paginate_by = 5

class LaundryShirtsOrderDetail(DetailView):
    context_object_name = 'shirts_order'
    template_name = 'launder/shirts_detail.html'
    model = LaundryShirtsOrder