from pyexpat import model
from django.contrib.auth import forms as auth_forms
from pyrsistent import field
from users.models import User
from accounts.models import Room,Chat
from django import forms


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    """ユーザー登録用フォーム"""

    class Meta:
        model = User
        fields = ('username',"age")
        #年齢を追加することに成功！

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class RoomAddForm(forms.ModelForm):
    """ルーム作成"""
    room = forms.CharField(
        label='ルーム名',
        max_length=10,
        required=True, 
    )
    meta = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True, 
        queryset=User.objects,
        label='ユーザー追加'
    )
    class Meta:
        model = Room
        fields = '__all__'

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'last_name',
            'first_name',
        ]

    def __init__(self, email=None, first_name=None, last_name=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        if email:
            self.fields['email'].widget.attrs['value'] = email
        if first_name:
            self.fields['first_name'].widget.attrs['value'] = first_name
        if last_name:
            self.fields['last_name'].widget.attrs['value'] = last_name

    def update(self, user):
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()