from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^campaign.json$', 'svc.views.campaign'),
    (r'^submit/$', 'svc.views.submit'),
    (r'^results.(?P<format>\w+)$', 'svc.views.results'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^form.html$',            'direct_to_template', {'template': 'svc/form.html'}),
)