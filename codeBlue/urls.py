
from django.conf.urls import url
from django.contrib import admin

from presentacion import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
    url(r'^oauth2callback$', views.calendar_auth_return, name="index"),
    url(r'^calendar/$', views.calendar, name="calendar"),
    url(r'^calendar/add_event/(?P<event_id>[0-9]+)/$', views.calendar_add_event, name="add_event"),
]
