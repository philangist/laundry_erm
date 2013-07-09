from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
    url(r'^wash_fold/', 'launder.views.wash_fold_view'),
    url(r'^dry_clean/', 'launder.views.dry_clean_view'),
    url(r'^shirts/', 'launder.views.shirts_view'),
	url(r'^$', 'launder.views.index')
)
