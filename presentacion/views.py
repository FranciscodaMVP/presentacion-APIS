import httplib2

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage

from .models import CredentialsModel, Event

# Create your views here.

FLOW = OAuth2WebServerFlow(
    settings.GOOGLE_OAUTH2_CLIENT_ID,
    settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://127.0.0.1:8000/oauth2callback'
)

def index(request):
    return render(request, 'expo.html')

def calendar(request):
    context = { 'events' : Event.objects.all() }
    return render(request, 'calendar.html', context)

def calendar_add_event(request, event_id):
    storage = DjangoORMStorage(
        CredentialsModel,
        'user',
        request.user,
        'credential'
    )
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)

        event = Event.objects.get(pk=event_id)
        calendar_service = build('calendar', 'v3', http=http)
        body = {
            'start': { "date": str(event.date) },
            'end': { "date": str(event.date) },
            'summary': event.summary
        }
        calendar_request = calendar_service.events().insert(
            calendarId='primary',
            body=body,
        )
        response = calendar_request.execute()
        return redirect('calendar')

def calendar_auth_return(request):
    #if not xsrfutil.validate_token(
            #settings.SECRET_KEY,
            #request.GET['state'],
            #request.user):
        #return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel, 'user', request.user, 'credential')
    storage.put(credential)
    return redirect('calendar')
