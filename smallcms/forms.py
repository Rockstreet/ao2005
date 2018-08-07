from registration.forms import RegistrationForm
from django import forms

class UserProfileRegistrationForm(RegistrationForm):

    name = forms.CharField(label='ФИО *', max_length=100, widget=forms.TextInput(attrs={'size':'40', 'class':'form-control'}))
    phone = forms.CharField(label='Телефон *', max_length=100, widget=forms.TextInput(attrs={'size':'40', 'class':'form-control'}))
    adres = forms.CharField(label='Адрес доставки', max_length=100,required=False, widget=forms.TextInput(attrs={'size':'40', 'class':'form-control'}))