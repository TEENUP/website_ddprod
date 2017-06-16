
from django import forms

class ContactForm(forms.Form):
	contact_name = forms.CharField(required = True)
	contact_email = forms.EmailField(required = True)
	contact_subject = forms.CharField(required = True)
	cotent = forms.CharField(required = True, widget = forms.Textarea)

