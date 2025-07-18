from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from collections import OrderedDict
from .models import Task
from pytz import timezone as pytz_timezone

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'style': 'width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; transition: border-color 0.2s ease; box-sizing: border-box;'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        field_order = ['email', 'password1', 'password2']
        self.fields = {k: self.fields[k] for k in field_order if k in self.fields}
        
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Create a password (minimum 8 characters)',
            'style': 'width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; transition: border-color 0.2s ease; box-sizing: border-box;'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password',
            'style': 'width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; transition: border-color 0.2s ease; box-sizing: border-box;'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Please enter a valid email address.')
            
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email address is already registered.')
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get('email')
        username = email.split('@')[0]
        
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user.username = username
        user.email = email
        
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'style': 'width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; transition: border-color 0.2s ease; box-sizing: border-box;'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'style': 'width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; transition: border-color 0.2s ease; box-sizing: border-box;'
        })
    )

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if timezone.is_naive(due_date):
            user_tz = pytz_timezone('America/Denver')
            due_date = timezone.make_aware(due_date) if timezone.is_naive(due_date) else due_date
        return due_date