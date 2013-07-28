from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	#wash_fold urls
	url(r'^wash_fold_form/$', 'launder.views.wash_fold_add_form'),
	url(r'^wash_fold_form/(?P<wash_fold_order>\d+)/$', 'launder.views.wash_fold_add_form'),
	url(r'^wash_fold/add/(?P<wash_fold_id>\d+)/$', 'launder.views.wash_fold_add'),
	url(r'^wash_fold/add/$', 'launder.views.wash_fold_add'),
	url(r'^wash_fold/$', 'launder.views.wash_fold'),
	url(r'^wash_fold/(?P<wash_fold_order>\d+)/$', 'launder.views.wash_fold_detail'),
	#dry_clean urls
	url(r'^dry_clean_form/$', 'launder.views.dry_clean_add_form'),
	url(r'^dry_clean_form/(?P<dry_clean_order>\d+)/$', 'launder.views.dry_clean_add_form'),
    url(r'^dry_clean/add/(?P<dry_clean_id>\d+)/$', 'launder.views.dry_clean_add'),
    url(r'^dry_clean/add/$', 'launder.views.dry_clean_add'),
    url(r'^dry_clean/$', 'launder.views.dry_clean'),
	url(r'^dry_clean/(?P<dry_clean_order>\d+)/$', 'launder.views.dry_clean_detail'),
	#shirts urls
	url(r'^shirts_form/$', 'launder.views.shirts_add_form'),
	url(r'^shirts_form/(?P<shirt_order>\d+)/$', 'launder.views.shirts_add_form'),
	url(r'^shirts/add/(?P<shirt_id>\d+)/$', 'launder.views.shirts_add'),
	url(r'^shirts/add/$', 'launder.views.shirts_add'),
    url(r'^shirts/$', 'launder.views.shirts'),
	url(r'^shirts/(?P<shirt_order>\d+)/$', 'launder.views.shirts_detail'),
	#index
	url(r'^$', 'launder.views.index')
)
