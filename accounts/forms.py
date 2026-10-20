from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from candidates.models import CandidateProfile
from recruiters.models import RecruiterProfile

User = get_user_model()


class CandidateRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}))
    headline = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python Full Stack Developer'}))
    skills = forms.CharField(max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, MySQL, React'}))
    preferred_location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Remote, New York, Bangalore'}))
    experience_years = forms.IntegerField(min_value=0, max_value=40, initial=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            CandidateProfile.objects.create(
                user=user,
                headline=self.cleaned_data.get('headline', ''),
                skills=self.cleaned_data.get('skills', ''),
                preferred_location=self.cleaned_data.get('preferred_location', ''),
                experience_years=self.cleaned_data.get('experience_years', 0),
            )
        return user


class RecruiterRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'recruiter@company.com'}))
    company_name = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company / Agency Name'}))
    company_website = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'}))
    company_location = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. San Francisco, CA'}))
    industry = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Information Technology / SaaS'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'recruiter'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            RecruiterProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_website=self.cleaned_data.get('company_website', ''),
                company_location=self.cleaned_data.get('company_location', ''),
                industry=self.cleaned_data.get('industry', ''),
                contact_email=user.email,
            )
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
