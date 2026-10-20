from django import forms
from .models import Job, JobSkill


class JobForm(forms.ModelForm):
    skills_input = forms.CharField(
        max_length=500,
        required=True,
        label="Required Skills",
        help_text="Enter comma-separated skills (e.g. Python, Django, MySQL, Docker, REST API)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, MySQL, Docker, REST API'})
    )

    class Meta:
        model = Job
        fields = [
            'title',
            'location',
            'work_arrangement',
            'employment_type',
            'experience_level',
            'min_salary',
            'max_salary',
            'status',
            'description',
            'requirements',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Full Stack Engineer'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. New York, NY or Remote'}),
            'work_arrangement': forms.Select(attrs={'class': 'form-select'}),
            'employment_type': forms.Select(attrs={'class': 'form-select'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'min_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 70000'}),
            'max_salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 110000'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detailed job description...'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Candidate qualifications, responsibilities...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_skills = self.instance.get_skills_list()
            self.fields['skills_input'].initial = ", ".join(current_skills)

    def save(self, recruiter, commit=True):
        job = super().save(commit=False)
        job.recruiter = recruiter
        if commit:
            job.save()
            # Save associated JobSkills
            skills_raw = self.cleaned_data.get('skills_input', '')
            skill_names = [s.strip() for s in skills_raw.split(',') if s.strip()]
            job.skills.all().delete()
            for s_name in skill_names:
                JobSkill.objects.create(job=job, skill_name=s_name)
        return job
