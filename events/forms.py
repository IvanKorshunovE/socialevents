from django import forms
from django.forms import ModelForm
from .models import Venue, Events

# Create a Venue Form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        # fields = '__all__'
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue' }),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address' }),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code' }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone' }),
            'web': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Web Site' }),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address' }),
        }

        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
        }


# Admin Superuser Event Form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Events
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }


# User event form (without selecting manager)
class EventForm(ModelForm):
    # We took out the manager label but the manager field is still in database.
    class Meta:
        model = Events
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Name'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Venue'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS',
            'venue': 'Venue',
            'attendees': 'Attendees',
            'description': '',
        }