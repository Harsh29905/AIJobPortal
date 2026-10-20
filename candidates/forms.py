from django import forms
from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = [
            'headline',
            'phone',
            'current_location',
            'preferred_location',
            'experience_years',
            'skills',
            'education',
            'bio',
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Backend Engineer | Python & Distributed Systems'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 019-2834'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State/Country'}),
            'preferred_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred location or Remote'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 50}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, MySQL, Docker, REST API'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'B.S. in Computer Science - University (2024)'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'A brief summary of your background, passions, and goals...'}),
        }


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['resume_file']
        widgets = {
            'resume_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }

    def clean_resume_file(self):
        resume = self.cleaned_data.get('resume_file')
        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF resumes are supported.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file size cannot exceed 5MB.")
        return resume
