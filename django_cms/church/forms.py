"""
Forms for Laver Transformation Ministries Church CMS
"""
from django import forms
from .models import (
    PrayerRequest, ContactMessage, NewsletterSubscriber
)


class PrayerRequestForm(forms.ModelForm):
    """Form for prayer requests"""
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'phone', 'request']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (Optional)'
            }),
            'request': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your prayer request...',
                'rows': 5,
                'required': True
            }),
        }


class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (Optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'rows': 5,
                'required': True
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Form for newsletter subscription"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
    )
    
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
