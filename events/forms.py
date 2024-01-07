from dataclasses import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Venue, Event

class VenueForm(ModelForm):
    class Meta:
        model= Venue
        fields= ("name", "city", "address", "province", "phone", "web", "email", "owner")  # can be also --- fields= "__all__"
        widgets= {
            "name": forms.TextInput(attrs={'class':'form-control'}),
            "city": forms.TextInput(attrs={'class':'form-control'}),
            "address": forms.TextInput(attrs={'class':'form-control'}),
            "province": forms.TextInput(attrs={'class':'form-control'}),
            "phone": forms.TextInput(attrs={'class':'form-control'}),
            "web": forms.URLInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class':'form-control'}),
            "owner": forms.HiddenInput(attrs={'class':'form-select'}),
        }

class EventForm(ModelForm):
    class Meta:
        model= Event
        fields= ("name", "event_date", "venue", "manager", "description", "event_image")
        labels= {
            "event_date": "Evenet Date in: YYYY-MM-DD HH:MM:SS",
        }
        widgets= {
            "name": forms.TextInput(attrs={'class':'form-control'}),
            "event_date": forms.DateTimeInput(attrs={'class':'form-control'}),
            "venue": forms.Select(attrs={'class':'form-select'}),
            "manager": forms.HiddenInput(attrs={'class':'form-select'}),
            "description": forms.Textarea(attrs={'class':'form-control'}),
            "event_image": forms.FileInput(attrs={'class':'form-control'}),
        }

