from django import forms

class UrlForm(forms.Form):
    url = forms.CharField(max_length=200)

class TransForm(forms.Form):
    text = forms.CharField(max_length=200, widget = forms.Textarea)
