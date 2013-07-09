from django.conf.urls import patterns, include, url

urlpatterns = patterns('poll.views',
    url(r'^wash_fold', 'wash_fold_view'),
    url(r'^dry_clean', 'dry_clean_view'),
    url(r'^shirts', 'shirts_view'),
    url(r'^$', 'index'),
)