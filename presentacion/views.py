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

from .models import CredentialsModel, DriveCredentialsModel, Event
from .forms import UrlForm


# Create your views here.

CALENDAR_FLOW = OAuth2WebServerFlow(
    settings.GOOGLE_OAUTH2_CLIENT_ID,
    settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri='http://localhost:8000/calendar/oauth2callback'
)

DRIVE_FLOW = OAuth2WebServerFlow(
    settings.GOOGLE_OAUTH2_CLIENT_ID,
    settings.GOOGLE_OAUTH2_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/drive.metadata.readonly',
    redirect_uri='http://localhost:8000/drive/oauth2callback'
)

def index(request):
    return render(request, 'expo.html')

def calendar(request):
    context = {
        'events': Event.objects.all(),
    }
    if CredentialsModel.objects.filter(user=request.user).count() > 0:
        context['have_cred'] = True
    else:
        context['have_cred'] = False
    return render(request, 'calendar.html', context)

def calendar_eventadded(request):
    context = {
        'events': Event.objects.all(),
        'event_added': True,
    }

    if CredentialsModel.objects.filter(user=request.user).count() > 0:
        context['have_cred'] = True
    else:
        context['have_cred'] = False
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
        CALENDAR_FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = CALENDAR_FLOW.step1_get_authorize_url()
        return redirect(authorize_url)
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
        return redirect('calendar_eventadded')

def calendar_auth_return(request):
    if not xsrfutil.validate_token(
            settings.SECRET_KEY,
            bytes(request.GET['state'], 'utf-8'),
            request.user):
        return  HttpResponseBadRequest()
    credential = CALENDAR_FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel, 'user', request.user, 'credential')
    storage.put(credential)
    return redirect('calendar')

def drive(request):
    context = {}

    storage = DjangoORMStorage(
        DriveCredentialsModel,
        'user',
        request.user,
        'credential'
    )
    credential = storage.get()
    if credential is None or credential.invalid == True:
        DRIVE_FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = DRIVE_FLOW.step1_get_authorize_url()
        return redirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)

        drive_service = build('drive', 'v3', http=http)
        drive_request = drive_service.files().list(
            pageSize = 10,
            fields = 'nextPageToken, files(id, name)'
        )
        results = drive_request.execute()
        drive_request = drive_service.files().list_next(drive_request, results)
        results = drive_request.execute()
        items = results.get('files', [])
        context['items'] = items
        return render(request, 'drive.html', context)

def drive_auth_return(request):
    if not xsrfutil.validate_token(
            settings.SECRET_KEY,
            bytes(request.GET['state'], 'utf-8'),
            request.user):
        return  HttpResponseBadRequest()
    credential = DRIVE_FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(DriveCredentialsModel, 'user', request.user, 'credential')
    storage.put(credential)
    return redirect('calendar')

def shortener(request):
    context = {}

    form = UrlForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            short_url = form.cleaned_data['url']

            url_service = build(
                'urlshortener',
                'v1',
                developerKey=settings.GOOGLE_API_KEY,
            )
            resp = url_service.url().get(shortUrl=short_url).execute()
            context['long_url'] = resp['longUrl']

    context['form'] = form
    return render(request, 'shortener.html', context)

def maps(request):
    return render(request, 'gmaps.html')

def translate(request):
    context = {}

    form = TransForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            trans = form.cleaned_data['text']

            url_service = build(
                'translate', 'v2',
                developerKey=settings.GOOGLE_API_KEY,
            )
            resp = url_service.translations().list(
                source='en',
                target='es',
                q=trans).execute()
            context['translated'] = resp['translations'][0]['translatedText']

    context['form'] = form
    return render(request, 'translate.html', context)
