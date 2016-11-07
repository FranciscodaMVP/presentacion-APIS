
from django.conf.urls import url
from django.contrib import admin
from presentacion.views import Main_view

from presentacion import views

urlpatterns = [
    url(r'^$', Main_view.as_view(), name='start'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name="index"),
]
