from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView


# all AJAX should be specified and should be in different file, not in views.py file,
# user a different file called ajax.py also update the url as /<appname>/ajax/<function>

urlpatterns = patterns('',
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'login.html'},
                           name='logout'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^favicon\.ico$', RedirectView.as_view(url='/static/media/complaints_fevicon.png')),
)

urlpatterns += patterns('ticket_tracker.views',
                        url(r'^$', 'custom_login', name='login'),

                        url(r'^ticket/$', 'ticket_register'),

                        url(r'^registration/$', 'registration', name='registration'),


                        url(r'^pending_ticket/$', 'pending_ticket', name='pending_ticket'),
                        url(r'^resolved_ticket/$', 'resolved_ticket', name='resolved_ticket'),

)

urlpatterns += patterns('ticket_tracker.ajax',
                        url(r'^ticket_tracker/ajax/update_ticket/$', 'update_ticket', name='update_ticket'),
                        url(r'^ticket_tracker/ajax/update_comment/$', 'update_comment', name='update_comment'),
)
