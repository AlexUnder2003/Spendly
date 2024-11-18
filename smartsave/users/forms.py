from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'address',
            'city',
            'gender'
            ]

        widgets = {
            'gender': forms.Select(choices=User.GENDERS),
        }

    username = forms.CharField(
        error_messages={'required': ''},
    )
