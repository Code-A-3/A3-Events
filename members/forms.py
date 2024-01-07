from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        help_texts = {
            'username': None,
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control',}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',}),
            'email': forms.EmailInput(attrs={'class': 'form-control',}),

        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    

