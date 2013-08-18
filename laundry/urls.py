from django.contrib.auth.decorators import(
	login_required,
	permission_required
)
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from launder.views import (
	DailyOperationsList,
	DailyOperationsDryCleaningArchive,
	DailyOperationsLaundryShirtsArchive,
	DailyOperationsWashFoldArchive,
	WashFoldCreate,
	WashFoldUpdate,
	WashFoldList,
	WashFoldDetail,
	DryCleaningCreate,
	DryCleaningUpdate,
	DryCleaningList,
	DryCleaningDetail,
	LaundryShirtsOrderCreate,
	LaundryShirtsOrderUpdate,
	LaundryShirtsOrderList,
	LaundryShirtsOrderDetail,
)
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	#daily_operations urls
	url(r'^$',
		login_required(DailyOperationsList.as_view()),
		name='daily_ops_list'),

	url(r'^daily_ops/dry_cleaning/',
		login_required(DailyOperationsDryCleaningArchive.as_view()),
		name='daily_ops_dry_cleaning_archive'),
	
	url(r'^daily_ops/shirts/$',
		login_required(DailyOperationsLaundryShirtsArchive.as_view()),
		name='daily_ops_shirts_archive'),
	
	url(r'^daily_ops/wash_fold/',
		login_required(DailyOperationsWashFoldArchive.as_view()),
		name='daily_ops_wash_fold_archive'),

	#wash and fold urls
	url(r'^wash_fold/add/(?P<pk>\d+)/$',
		login_required(WashFoldUpdate.as_view()),
		name='wash_fold_update'),

	url(r'^wash_fold/add/$',
		login_required(WashFoldCreate.as_view()),
		name='wash_fold_add'),
	
	url(r'^wash_fold/(?P<pk>\d+)/$',
		login_required(WashFoldDetail.as_view()),
		name='wash_fold_detail'),

	url(r'^wash_fold/$',
		login_required(WashFoldList.as_view()),
		name='wash_fold_list'),

	#dry clean urls
	url(r'^dry_cleaning/add/(?P<pk>\d+)/$',
		login_required(DryCleaningUpdate.as_view()),
		name='dry_cleaning_update'),

	url(r'^dry_cleaning/add/$',
		login_required(DryCleaningCreate.as_view()),
		name='dry_cleaning_add'),

	url(r'^dry_cleaning/(?P<pk>\d+)/$',
		login_required(DryCleaningDetail.as_view()),
		name='dry_cleaning_detail'),

	url(r'^dry_cleaning/$',
		login_required(DryCleaningList.as_view()),
		name='dry_cleaning_list'),
		
	#shirts urls
	url(r'^shirts/add/(?P<pk>\d+)/$',
		login_required(LaundryShirtsOrderUpdate.as_view()),
		name='shirts_update'),
		
	url(r'^shirts/add/$',
		login_required(LaundryShirtsOrderCreate.as_view()),
		name='shirts_add'),
		
	url(r'^shirts/(?P<pk>\d+)/$',
		login_required(LaundryShirtsOrderDetail.as_view()),
		name='shirts_detail'),
		
	url(r'^shirts/$',
		login_required(LaundryShirtsOrderList.as_view()),
		name='shirts_list'),
	#user auth
	url(r'^login/$',
		'django.contrib.auth.views.login',
		name="login"),
	url(r'^logout/$',
		'django.contrib.auth.views.logout',
		{'next_page': '/'},
		name="logout",)
)
