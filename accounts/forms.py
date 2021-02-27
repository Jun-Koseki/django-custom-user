from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """ 新規ユーザ登録フォーム """
    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """ アカウント編集フォーム """
    class Meta:
        model = User
        fields = {'username', 'email', 'bio', 'website'}

        widgets = {
            'bio': Textarea(attrs={'rows': 4, 'cols': 20})
        }
