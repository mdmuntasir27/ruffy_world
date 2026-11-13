from django import forms
from django.contrib.auth.models import User
from pets.models import Pet
from adoptions.models import AdoptionRequest
from store.models import Product, Order
from vets.models import Vet
from community.models import AdoptionPost, AdoptionInquiry
from accounts.models import UserProfile
from accounts.validators import validate_mobile_phone, validate_email_format


class AdminLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Admin Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class PetAdminForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 'animal_type', 'breed', 'age', 'gender',
            'location', 'price', 'price_type', 'status',
            'description', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pet name'}),
            'animal_type': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Persian Cat'}),
            'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 years 3 months'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Area'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in BDT (optional)'}),
            'price_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Pet details and personality...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in BDT'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Available stock units'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Product description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'shipping_address', 'phone', 'full_name']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            return validate_mobile_phone(phone)
        return phone


class VetAdminForm(forms.ModelForm):
    class Meta:
        model = Vet
        fields = [
            'name', 'specialization', 'phone', 'email',
            'clinic_address', 'shift', 'is_available', 'bio', 'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dr. Full Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Small Animal Surgery'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vet@example.com'}),
            'clinic_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clinic address'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Experience, qualifications...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return validate_mobile_phone(phone)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return validate_email_format(email)
        return email


class AdoptionRequestStatusForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CommunityPostStatusForm(forms.ModelForm):
    class Meta:
        model = AdoptionPost
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class CommunityInquiryStatusForm(forms.ModelForm):
    class Meta:
        model = AdoptionInquiry
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class UserAdminEditForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '01XXXXXXXXX'})
    )
    is_staff = forms.BooleanField(
        required=False,
        label='Staff Status (Admin Panel Access)',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_active = forms.BooleanField(
        required=False,
        label='Active Account',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_staff', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            profile, _ = UserProfile.objects.get_or_create(user=self.instance)
            self.fields['phone'].initial = profile.phone

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
        user = super().save(commit=commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.save()
        return user
