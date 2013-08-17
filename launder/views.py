from datetime import datetime
import datetime as dt
from itertools import chain

from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
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

class DailyOperationsView(ListView):
    context_object_name = 'daily_orders_list'
    todays_date = dt.date.today()
    wash_fold_set = WashFoldOrder.objects.all()#filter(pk=-1)#date=todays_date)
    dry_clean_set = DryCleaning.objects.all()#filter(pk=-1)#date=todays_date)
    shirts_set = LaundryShirtsOrder.objects.all()#filter(pk=-1)#date=todays_date)
    queryset =  list(chain(
        wash_fold_set,
        dry_clean_set,
        shirts_set,
        )
    )
    logger.debug('queryset: %s' % str (queryset))
    template_name = 'index.html'

class WashFoldCreate(CreateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'

class WashFoldUpdate(UpdateView):
    model = WashFoldOrder
    form_class = WashFoldOrderForm
    template_name = 'launder/wash_fold_form.html'

class WashFoldList(ListView):
    template_name = 'launder/wash_fold_list.html'
    model = WashFoldOrder

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
    template_name = 'launder/dry_cleaning_list.html'
    model = DryCleaning

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
    template_name = 'launder/shirts_list.html'
    model = LaundryShirtsOrder

class LaundryShirtsOrderDetail(DetailView):
    context_object_name = 'shirts_order'
    template_name = 'launder/shirts_detail.html'
    model = LaundryShirtsOrder

def index(request):
    return render_to_response('index.html')
