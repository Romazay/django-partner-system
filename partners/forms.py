from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Partner, PromoCode


class PartnerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1',
                  'password2', 'company_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Partner.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                phone=self.cleaned_data['phone']
            )
        return user


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['discount_percent', 'is_active']
        widgets = {
            'discount_percent': forms.NumberInput(attrs={'min': 1, 'max': 100}),
        }
