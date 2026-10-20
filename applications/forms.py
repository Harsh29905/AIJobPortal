from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    use_profile_resume = forms.BooleanField(
        required=False,
        initial=True,
        label="Use resume from my profile"
    )

    class Meta:
        model = Application
        fields = ['cover_letter', 'resume_file']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share why you are a great fit for this position...'
            }),
            'resume_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
        }

    def clean_resume_file(self):
        resume = self.cleaned_data.get('resume_file')
        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are supported.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size cannot exceed 5MB.")
        return resume
