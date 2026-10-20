from django import forms
from .models import RecruiterProfile


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = [
            'company_name',
            'company_website',
            'company_location',
            'industry',
            'contact_email',
            'company_description',
            'company_logo',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Acme Corp'}),
            'company_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://acme.com'}),
            'company_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'San Francisco, CA'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fintech, Cloud, Healthcare'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'careers@acme.com'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'About the company, vision, and team culture...'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
