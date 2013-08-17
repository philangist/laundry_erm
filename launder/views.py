from datetime import datetime
import datetime as dt
from itertools import chain
from django.db.models import Q

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

class DailyOperationsList(ListView):
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
    template_name = 'index.html'

class DailyOperationsDryCleaningArchive(ArchiveIndexView):
    date_field = 'date'
    queryset = DryCleaning.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'

class DailyOperationsLaundryShirtsArchive(ArchiveIndexView):
    date_field = 'date'
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'

class DailyOperationsWashFoldArchive(ArchiveIndexView):
    date_field = 'date'
    queryset = WashFoldOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/daily_ops_archive.html'

class WashFoldCreate(CreateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'

class WashFoldUpdate(UpdateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'

class WashFoldList(ListView):
    queryset= WashFoldOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/wash_fold_list.html'

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

class DryCleaningList(ListView):
    queryset= DryCleaning.objects.all().filter(payment_finalized=True)
    template_name = 'launder/dry_cleaning_list.html'

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

class LaundryShirtsOrderList(ListView):
    queryset= LaundryShirtsOrder.objects.all().filter(payment_finalized=True)
    template_name = 'launder/shirts_list.html'

class LaundryShirtsOrderDetail(DetailView):
    context_object_name = 'shirts_order'
    template_name = 'launder/shirts_detail.html'
    model = LaundryShirtsOrder

def index(request):
    return render_to_response('index.html')
