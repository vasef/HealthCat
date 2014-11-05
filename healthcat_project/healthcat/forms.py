from django import forms
from django.contrib.auth.models import User
from models import *

class IconName(object):
    def get_icon_name(self):
        return self._icon_name
    def set_icon_name(self, value):
        self._icon_name = value
    icon_name = property(get_icon_name, set_icon_name)

class CharFieldWithIcon(forms.CharField, IconName):
    pass

class Tooltip(object):
    def get_tooltip(self):
        return self._tooltip
    def set_tooltip(self, value):
        self._tooltip = value
    tooltip = property(get_tooltip, set_tooltip)

class CharFieldWithIconAndTooltip(forms.CharField, IconName, Tooltip):
    pass

class ProfileForm(forms.ModelForm):
    username = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))
    password2 = forms.CharField(max_length = 200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Confirm Password...'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget=forms.PasswordInput(attrs={'class':'input-block-level', 'placeholder':'Password...'}))
    class Meta:
        model = Owner
        exclude = ('user',)
        widgets = {
                   'zip_code': forms.TextInput(attrs={'placeholder': 'Zip Code...'}),
                   'photo': forms.FileInput(),
                  }

class RegistrationForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.EmailField(max_length = 40, 
                                label='Email', 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: alex@healthcat.com'})
                                )
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'})
                                )
    password2 = forms.CharField(max_length = 200,
                                label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class + ' ' + required_css_class, 
                                           'placeholder':'eg: 1234'})
                                )
    first_name = forms.CharField(max_length = 20, 
                                 label='First Name',
                                 widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + required_css_class, 
                                           'placeholder':'eg: Alex'})
                                )
    last_name = forms.CharField(required=False, 
                                label='Last Name',
                                max_length = 20, 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control', 
                                           'placeholder':'eg: Fischer'})
                                )
    zip_code = CharFieldWithIconAndTooltip(required=False, max_length = 5, 
                                label='Zip Code', 
                                widget=forms.TextInput(
                                    attrs={'class':'form-control' + ' ' + error_css_class, 
                                           'placeholder':'eg: 15213'})
                                )
    class Meta:
        model = User
        fields = ("first_name","last_name", "username", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['zip_code'].icon_name = 'glyphicon glyphicon-question-sign'
        self.fields['zip_code'].tooltip = 'To compare your pets to pets in your area.'

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(max_length = 40 , widget=forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Email Address...'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(username__exact=email):
            raise forms.ValidationError("Sorry, we do not have an accout with that email.")
        return email
