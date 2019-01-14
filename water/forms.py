from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Your name', max_length=100)
    email = forms.CharField(label='Your email',max_length=100)
    phone = forms.CharField(label="Your Phone Number",max_length=100)
    address = forms.CharField(max_length=200)
    country = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    city= forms.CharField(max_length=50)
    password = forms.CharField(max_length=100)
