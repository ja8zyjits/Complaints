__author__ = 'jitesh.nair'
from django.conf.urls import patterns, include, url
from ticket_tracker import views

urlpatterns = patterns('',
                       url(r'^complaints/$', views.complaints_register),
                       url(r'^login/$', views.custom_login, name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'template_name': 'login.html'},
                           name='logout'),
                       url(r'^registration/$', views.registration, name='registration'),

                       url(r'^service_dashboard/$', views.dashboard,
                           name='dashboard'),
                       url(r'^resolved_dashboard/$', views.resolved_dashboard,
                           name='resolved_dashboard'),

                       url(r'^update/$', views.update, name='update'),
                       url(r'^update_comments/$', views.update_comments, name='update_comments'),
)