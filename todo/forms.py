from django import forms
import re
from django.contrib.auth.models import User
from todo.models import PRIORITY, STATE

password_regex = re.compile(r'^.*(?=.{4,}).*$')

class UserCreationForm(forms.Form):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'Username','class':'full-width','autocomplete':'off'}
        ),
        required=True,
    )
	
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder':'Password','autocomplete':'off'}
        ),
        required=True,
    )

    def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username = username)
		except User.DoesNotExist:
			return username.strip()
		raise forms.ValidationError("A user with this username already exists.")

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        if password != '':
            if not password_regex.match( password ):
                raise forms.ValidationError('Password must be at least 4 characters long.')
            return password.strip()
        
class LoginForm(forms.ModelForm):
    """ Require email address when a user signs up """
  
    email = forms.EmailField(label='Email address', max_length=75)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput, error_messages={'required': u'Please enter password'}
    )

    class Meta:
        model = User
        fields = ('email',) 

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists.")
        except User.DoesNotExist:
            return email

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        if password != '':
            if not password_regex.match( password ):
                raise forms.ValidationError('Password must have a minimum length of 4.')
        return password.strip()

class TodoForm(forms.Form):
    name = forms.CharField(
		widget=forms.TextInput(
            attrs={'placeholder':'Name','class':'full-width','autocomplete':'off'}
        ),
        required=True,
    )
    description = forms.CharField(widget=forms.Textarea)
    priority = forms.ChoiceField(widget=forms.RadioSelect, choices=PRIORITY)
    state = forms.ChoiceField(choices=STATE)
    task_date = forms.CharField()
    
