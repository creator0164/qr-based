from django import forms
from account.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=255, help_text='Required. Add a username.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            account = User.objects.exclude(
                pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            'Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            account = User.objects.exclude(
                pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            'username "%s" is already in use.' % account)


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            try:
                username = self.cleaned_data['username']
                password = self.cleaned_data['password']
                user = authenticate(username=username, password=password)
                user_status = User.objects.get(username=username)

                if not user_status.is_active:
                    raise forms.ValidationError('Not Activated')

                if user is None:
                    raise forms.ValidationError(
                        'Username and Password are not matched')
            except User.DoesNotExist:
                raise forms.ValidationError('Username does not exist')
