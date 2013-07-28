from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from  django.core.urlresolvers import reverse

from launder.forms import WashFoldOrderForm
from launder.models import WashFoldOrder, DryCleaning, LaundryShirtsOrder

import logger_factory

logger = logger_factory.logger_factory('views')

def make_wash_fold_instance(request):
	logger.info('entered make_wash_fold_instance')
	wash_fold_instance = WashFoldOrder(
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		phone_number = request.POST['phone_number'],
		address = request.POST['address'],
		total_cost = float(request.POST['total_cost']),
		payment_method = request.POST['payment_method'],
		payment_finalized = request.POST['payment_finalized']
	)
	logger.info('wash_fold_instance created')
	return wash_fold_instance

def edit_wash_fold_instance(request, wash_fold_id):
	logger.info('entered edit_wash_fold_instance')
	wash_fold_instance = WashFoldOrder.objects.get(pk=wash_fold_id)
	logger.info('wash_fold_instance.__dict__: %s' % str(wash_fold_instance.__dict__))
	wash_fold_instance.first_name = request.POST['first_name']
	wash_fold_instance.last_name = request.POST['last_name']
	wash_fold_instance.phone_number = request.POST['phone_number']
	wash_fold_instance.address = request.POST['address']
	wash_fold_instance.total_cost = float(request.POST['total_cost'])
	wash_fold_instance.payment_method = request.POST['payment_method']
	wash_fold_instance.payment_finalized = request.POST['payment_finalized']
	logger.info('wash_fold_instance edited')
	logger.info('edited wash_fold_instance.__dict__: %s' % str(wash_fold_instance.__dict__))
	return wash_fold_instance

def make_dry_clean_instance(request):
	logger.info('entered make_dry_clean_instance')
	dry_cleaning_instance = DryCleaning(
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		phone_number = request.POST['phone_number'],
		address = request.POST['address'],
		garment_type = request.POST['garment_type'],
		garment_amount= int(request.POST['garment_amount']),
		total_cost = float(request.POST['total_cost']),
		payment_method = request.POST['payment_method'],
		payment_finalized = request.POST['payment_finalized']
	)
	logger.info('dry_cleaning_instance created: %s' % str(dry_cleaning_instance.__dict__))
	return dry_cleaning_instance

def edit_dry_clean_instance(request, dry_clean_id):
	logger.info('entered edit_dry_clean_instance')
	dry_clean_instance = WashFoldOrder.objects.get(pk=dry_clean_id)
	logger.info('dry_clean_instance.__dict__: %s' % str(dry_clean_instance.__dict__))
	dry_clean_instance.first_name = request.POST['first_name']
	dry_clean_instance.last_name = request.POST['last_name']
	dry_clean_instance.phone_number = request.POST['phone_number']
	dry_clean_instance.address = request.POST['address']
	dry_clean_instance.garment_type = float(request.POST['garment_type'])
	dry_clean_instance.garment_amount = float(request.POST['garment_amount'])
	dry_clean_instance.total_cost = float(request.POST['total_cost'])
	dry_clean_instance.payment_method = request.POST['payment_method']
	dry_clean_instance.payment_finalized = request.POST['payment_finalized']
	logger.info('dry_clean_instance edited')
	logger.info('edited dry_clean_instance.__dict__: %s' % str(dry_clean_instance.__dict__))
	return dry_clean_instance

def make_shirts_instance(request):
	logger.info('entered make_shirts_instance')
	shirts_instance = LaundryShirtsOrder(
		first_name = request.POST['first_name'],
		last_name = request.POST['last_name'],
		phone_number = request.POST['phone_number'],
		address = request.POST['address'],
		shirts_amount = request.POST['shirts_amount'],
		shirts_price = request.POST['shirts_price'],
		starched = request.POST['starched'],
		total_cost = request.POST['total_cost'],
		payment_method = request.POST['payment_method'],
		payment_finalized = request.POST['payment_finalized']
	)
	logger.info('shirts_instance created')
	return shirts_instance

def edit_shirts_instance(request, shirt_id):
	logger.info('entered edit_shirt_instance')
	shirt_instance = LaundryShirtsOrder.objects.get(pk=shirt_id)
	logger.info('shirt_instance.__dict__: %s' % str(shirt_instance.__dict__))
	shirt_instance.first_name = request.POST['first_name']
	shirt_instance.last_name = request.POST['last_name']
	shirt_instance.phone_number = request.POST['phone_number']
	shirt_instance.address = request.POST['address']
	shirt_instance.shirts_amount = int(request.POST['shirts_amount'])
	shirt_instance.shirts_price = float(request.POST['shirts_price'])
	shirt_instance.starched = bool(request.POST['starched'])
	shirt_instance.total_cost = float(request.POST['total_cost'])
	shirt_instance.payment_method = request.POST['payment_method']
	shirt_instance.payment_finalized = bool(request.POST['payment_finalized'])
	logger.info('shirt_instance edited')
	logger.info('edited shirt_instance.__dict__: %s' % str(shirt_instance.__dict__))
	return shirt_instance

def dry_clean(request):
	orders = DryCleaning.objects.all()
	return render_to_response('dry_clean.html', 
		{'orders' : orders}
	)

def dry_clean_detail(request, dry_clean_order):
	dry_clean_order = get_object_or_404(DryCleaning, pk=dry_clean_order)
	return render_to_response('dry_clean_detail.html',
		{'dry_clean_order' : dry_clean_order}
	)

def dry_clean_add_form(request, dry_clean_order=None):
	if dry_clean_order != None:
		dry_clean_order = get_object_or_404(DryCleaning, pk=dry_clean_order)
	return render(request, 'dry_clean_form.html', 
		{'dry_clean_order' : dry_clean_order}
	)

def dry_clean_add(request):
	logger.info("method: %s" % request.method)
	if request.method == 'POST':
		logger.info("POST params: %s" % str(request.POST))
		try:
			logger.info('entered try clause')
			dry_cleaning_instance = make_dry_clean_instance(request)
			dry_cleaning_instance.save()
			logger.info("New DryCleaning instance saved")
			return HttpResponseRedirect(reverse(dry_clean))
		except:
			logger.info('entered except clause')
			logger.info("New DryCleaning order addition failed")
			return HttpResponseRedirect(reverse(dry_clean_add_form))
	logger.info("dry_clean_add not a POST request")
	return HttpResponseRedirect('/')

def wash_fold(request):
	orders = WashFoldOrder.objects.all()
	return render_to_response('wash_fold.html', 
		{'orders' : orders}
	)

def wash_fold_detail(request, wash_fold_order):
	wash_fold_order = get_object_or_404(WashFoldOrder, pk=wash_fold_order)
	return render_to_response('wash_fold_detail.html',
		{'wash_fold_order' : wash_fold_order}
	)

def wash_fold_add_form(request, wash_fold_order=None):
	if wash_fold_order is not None:
		wash_fold_order = get_object_or_404(WashFoldOrder, pk=wash_fold_order)
	return render(request, 'wash_fold_form.html', 
		{'wash_fold_order' : wash_fold_order }
	)

def wash_fold_add(request, wash_fold_id=None):
	logger.info("method: %s" % request.method)
	if request.method == 'POST':
		logger.info("POST params: %s" % str(request.POST))
		try:
			logger.info('entered try clause')
			if wash_fold_id is not None:
				logger.info('updating wash_fold_instance')
				logger.info('wash_fold_id = %d, type = %s' % (int(wash_fold_id), str(type(wash_fold_id))))
				wash_fold_instance = edit_wash_fold_instance(request, wash_fold_id)
				logger.info('wash_fold_instance edited')
			else:
				wash_fold_instance = make_wash_fold_instance(request)
			wash_fold_instance.save()
			logger.info("New WashFoldOrder instance saved")
			return HttpResponseRedirect(reverse(wash_fold))
		except:
			logger.info('entered except clause')
			logger.info("New WashFoldOrder order addition failed")
			return HttpResponseRedirect(reverse(wash_fold_add_form))
	logger.info("wash_fold_add not a POST request")
	return HttpResponseRedirect('/')

def shirts(request):
	orders = LaundryShirtsOrder.objects.all()
	return render_to_response('shirts.html', 
		{'orders' : orders}
	)

def shirts_detail(request, shirt_order):
	shirt_order = get_object_or_404(LaundryShirtsOrder, pk=shirt_order)
	return render_to_response('shirts_detail.html',
		{'shirt_order' : shirt_order}
	)

def shirts_add_form(request, shirt_order=None):
	if shirt_order is not None:
		shirt_order = get_object_or_404(LaundryShirtsOrder, pk=shirt_order)
	return render(request, 'shirts_form.html', 
		{'shirt_order' : shirt_order}
	)

def shirts_add(request, shirt_id=None):
	logger.info("method: %s" % request.method)
	if request.method == 'POST':
		logger.info("POST params: %s" % str(request.POST))
		try:
			logger.info('entered try clause')
			if shirt_id is not None:
				logger.info('updating shirt')
				logger.info('shirt_id = %d, type = %s' % (int(shirt_id), str(type(shirt_id))))
				shirt = edit_shirts_instance(request, shirt_id)
				logger.info('shirts edited')
			else:
				shirt = make_shirts_instance(request)
			shirt.save()
			logger.info("New LaundryShirtsOrder instance saved")
			return HttpResponseRedirect(reverse(shirts))
		except:
			logger.info('entered except clause')
			logger.info("New LaundryShirtsOrder order addition failed")
			return HttpResponseRedirect(reverse(shirts_add_form))
	logger.info("shirts_add not a POST request")
	return HttpResponseRedirect('/')


def index(request):
	return render_to_response('index.html')
