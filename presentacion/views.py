from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
# Create your views here.

class Main_view(TemplateView):
    template_name='main.html'
