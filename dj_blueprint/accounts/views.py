from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic import CreateView

class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': 'Passwords do not match',
        'username_taken' : 'This username is already taken',
        'email_taken': 'thos email is already taken',
    }
    password = forms.CharField(label='Password',max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Confirm Password',max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email','password', 'password1')
        widgets = {
            'username': forms.TextInput(
				attrs={
					'class': 'form-control'
					}
				),
            'email': forms.EmailInput(
				attrs={
					'class': 'form-control'
					}
				)
			}

    def clean_username(self):
        username = self.cleaned_data['username']
        q = User.objects.filter(username=username)
        if q.exists():
            raise forms.ValidationError(self.error_messages['username_taken'],code='username_taken')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        q = User.objects.filter(email=email)
        if q.exists():
            raise forms.ValidationError(self.error_messages['email_taken'],code='email_taken')
        return email

    def clean_password1(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password1')
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],code='password_mismatch')
        return pass2
        
    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password',error)
            

    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = UsernameField(label='Username' ,max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    fields = ('username', 'password')
    


class UserRegistrationView(CreateView):
    form_class = UserForm
    template_name = 'register.html'

    def get_success_url(self):
        return reverse('login')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
