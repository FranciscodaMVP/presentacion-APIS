
from django.conf.urls import url
from django.contrib import admin

from presentacion import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),

    # Calendar
    url(r'^calendar/$', views.calendar, name="calendar"),
    url(r'^calendar/event_added/$', views.calendar_eventadded, name="calendar_eventadded"),
    url(r'^calendar/add_event/(?P<event_id>[0-9]+)/$', views.calendar_add_event, name="add_event"),
    url(r'^calendar/oauth2callback$', views.calendar_auth_return, name="calendar_auth_return"),

    # URL shortener
    url(r'^shortener/$', views.shortener, name="shortener"),

    # Google Maps
    url(r'^maps/$', views.maps, name="gmaps"),
]
