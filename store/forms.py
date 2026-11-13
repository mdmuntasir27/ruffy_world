from django import forms
from .models import Order
from accounts.validators import validate_mobile_phone


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment (Instant Dummy Gateway)'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'}),
        initial='cod',
        label='Payment Method'
    )

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'shipping_address', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 01XXXXXXXXX',
                'required': True,
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'House, Road, Area, City, Postcode...',
                'required': True,
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return validate_mobile_phone(phone)
