from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse


from launder.models import WashFoldOrder, DryCleaningForm, LaundryShirtsOrder

def wash_fold_view(request):
	orders = WashFoldOrder.objects.all()[:5]
	return render_to_response('wash_fold.html')

def dry_clean_view(request):
	orders = DryCleaningForm.objects.all()[:5]
	return render_to_response('dry_clean.html')

def launder_shirts_view(request):
	orders = LaundryShirtsOrder.objects.all()[:5]
	return render_to_response('shirts.html')

def index(request):
	return render_to_response('index.html')
