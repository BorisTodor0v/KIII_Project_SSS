from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:

        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['username'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Surname'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['email'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password'].widget.attrs.update({'autocomplete': 'new-password'})
        for field in self.visible_fields():
            field.label = ''
            field.field.widget.attrs["class"] = "form-control mt-2"
