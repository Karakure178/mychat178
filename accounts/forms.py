from django.contrib.auth import forms as auth_forms

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