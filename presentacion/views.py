from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
# Create your views here.

def index(request):
    return render(request, 'expo.html')
