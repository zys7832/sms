from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sms.views.index', name='index'),
    url(r'^login/$', 'sms.views.login', name='login'),
    url(r'^grade/(\d+)/$', 'sms.views.get_grade', name='grade'),
    url(r'^klass/(\d+)/$', 'sms.views.get_klass', name='klass'),
    url(r'^sendmail/$', 'sms.views.send_mail', name='sendmail'),
    url(r'^validator/([\w+\.?]+)/(\w+)/$','sms.views.validator',name='validator'),
    url(r'^register/$','sms.views.register_user',name='register'),
    url(r'^rpass/$','sms.views.reset_password',name='reset_password'),
    url(r'^page/([\w+\.?]+)/(\w+)/$','sms.views.page',name='page'),
    url(r'^action/([\w+\.?]+)/(\w+)/$','sms.views.action',name='action'),
    url(r'^datas/([\w+\.?]+)/(\w+)/$','sms.views.datas',name='datas'),
    url(r'^items/([\w+\.?]+)/(\w+)/$','sms.views.items',name='items'),
    url(r'^ajax_tree_items/([\w+\.?]+)/(\w+)/(\w+)/$','sms.views.ajax_tree_items',name='ajax_tree_items'),
    url(r'^admin/', include(admin.site.urls))
)
