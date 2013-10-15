from django.contrib.auth.decorators import(
    login_required,
    permission_required
)
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from launder.views import (
    get_customer_contact_info,
    set_customer_contact_info,
    LaundryIndex,
    DailyOperationsArchive,
    DailyOperationsList,
    DailyOperationsDateView,
    DailyOperationsDryCleaningArchive,
    DailyOperationsLaundryShirtsArchive,
    DailyOperationsWashFoldArchive,
    DailyOperationsProductsList,
    DailyOperationsProductsDateList,
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
    ProductCreate,
    ProductUpdate,
    ProductDetail,
    ProductList,
    CustomerOrdersList,
    UserCreate,
    PrintOrder,
)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^get_customer_contact_info/$',
        get_customer_contact_info,
        name='get_customer_contact_info'),

    url(r'^set_customer_contact_info/$',
        set_customer_contact_info,
        name='set_customer_contact_info'),

    #daily_operations urls
    url(r'^$',
        login_required(LaundryIndex.as_view()),
        name='index'),

    url(r'^archive/$',
        login_required(DailyOperationsArchive.as_view()),
        name='archive'),

    url(r'^daily_ops/products/(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)/$',
        login_required(DailyOperationsProductsDateList.as_view()),
        name='daily_ops_products_list_by_date'),

    url(r'^daily_ops/(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)/$',
        login_required(DailyOperationsDateView.as_view()),
        name='daily_ops_date_view'),

    url(r'^daily_ops/dry_cleaning/',
        login_required(DailyOperationsDryCleaningArchive.as_view()),
        name='daily_ops_dry_cleaning_archive'),

    url(r'^daily_ops/shirts/$',
        login_required(DailyOperationsLaundryShirtsArchive.as_view()),
        name='daily_ops_shirts_archive'),

    url(r'^daily_ops/wash_fold/',
        login_required(DailyOperationsWashFoldArchive.as_view()),
        name='daily_ops_wash_fold_archive'),

    url(r'^daily_ops/products/',
        login_required(DailyOperationsProductsList.as_view()),
        name='daily_ops_products_list'),


    url(r'^daily_ops/$',
        login_required(DailyOperationsList.as_view()),
        name='daily_ops_dates_list'),


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

    url(r'^product/add/(?P<pk>\d+)/$',
        login_required(ProductUpdate.as_view()),
        name='product_update'),

    url(r'^product/add/$',
        login_required(ProductCreate.as_view()),
        name='product_add'),

    url(r'^product/(?P<pk>\d+)/$',
        login_required(ProductDetail.as_view()),
        name='product_detail'),

    url(r'^product/$',
        login_required(ProductList.as_view()),
        name='product_list'),

    url(r'^customers/(?P<customer_name_slug>.+)/$',
        login_required(CustomerOrdersList.as_view()),
        name='customer_order_list'),

    url(r'^print/([a-zA-Z0-9_]+)/(\d+)/$',
        login_required(PrintOrder.as_view()),
        name='print_order'),

    #user auth
    url(r'^login/$',
        'django.contrib.auth.views.login',
        name='login'),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout',),

    url(r'^user/create/$',
        login_required(UserCreate.as_view()),
        name='user_create',),

)
