import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import UserProfile
from .validators import validate_mobile_phone, validate_email_format, validate_password_strength


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email address (e.g. user@example.com)', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. 01XXXXXXXXX', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return validate_email_format(email)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return validate_mobile_phone(phone)

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password_strength(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'phone': self.cleaned_data.get('phone', '')}
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'location']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 01XXXXXXXXX'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'A short bio...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city/area'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return validate_email_format(email)
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            return validate_mobile_phone(phone)
        return phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile


class ForgotPasswordLookupForm(forms.Form):
    identity = forms.CharField(
        max_length=150,
        required=True,
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registered username or email',
            'autofocus': True,
        })
    )

    def clean_identity(self):
        identity = self.cleaned_data.get('identity', '').strip()
        user = User.objects.filter(
            Q(username__iexact=identity) | Q(email__iexact=identity)
        ).first()
        if not user:
            raise forms.ValidationError("No registered account found with that username or email address.")
        self.matched_user = user
        return identity


class DirectResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password1',
            'placeholder': 'Enter new strong password',
            'autocomplete': 'new-password',
        })
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'id_password2',
            'placeholder': 'Re-enter your new password',
            'autocomplete': 'new-password',
        })
    )

    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        validate_password_strength(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            self.add_error('new_password2', "The two password fields didn't match.")
        return cleaned_data


class RuffySetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        validate_password_strength(password)
        return password
