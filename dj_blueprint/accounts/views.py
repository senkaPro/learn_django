from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.urls.base import reverse
from django.views.generic import CreateView

class UserForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(),required=True)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(),required=True)
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        q = User.objects.filter(username=username)
        if q.exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        q = User.objects.filter(email=email)
        if q.exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean_password(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Passwords do not match')
        password = password_validation(pass1)
        return password

    def save(self, commit=True, *args, **kwargs):
        user = super(UserForm, self).save(commit=False, *args, **kwargs)
        password = self.cleaned_data['password2']
        # user.username = self.cleaned_data['username']
        # user.email = self.cleaned_data['email']
        user.set_password(password)
        if commit:
            user.save()
        return user


class UserRegistrationView(CreateView):
    form_class = UserForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('login')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
