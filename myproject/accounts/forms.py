from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model




class CustomUserCreationForm(UserCreationForm):
    class Meta:

        model = CustomUser

        fields = ('username', 'email', 'password1', 'password2')


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="新しいパスワード",
        widget=forms.PasswordInput,
        )
    new_password2 = forms.CharField(
        label="新しいパスワード (確認)",
        widget=forms.PasswordInput,
    )


class UsernameChangeForm(forms.Form):
    new_username = forms.CharField(label='新しいユーザー名', max_length=150)

    def clean_new_username(self):
        new_username = self.cleaned_data['new_username']
        if not new_username:
            raise forms.ValidationError('ユーザー名を入力してください。')
        if len(new_username) < 4:
            raise forms.ValidationError('ユーザー名は4文字以上で入力してください。')
        if not new_username.isalnum():
            raise forms.ValidationError('ユーザー名は英数字のみで入力してください。')
        if CustomUser.objects.filter(username=new_username).exists():
            raise forms.ValidationError([
                'そのユーザー名はすでに登録されています。',
                'ほかのユーザー名にしてください。'
            ])
        return new_username





class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='登録済みのメールアドレス', max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        CustomUser = get_user_model()
        if not CustomUser.objects.filter(email=email).exists():
            self.add_error(None, 'このメールアドレスは登録されていません')
        return email


from django import forms
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class ContactForm(forms.Form):
    name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "お名前",
        }),
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "メールアドレス",
        }),
    )
    message = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "お問い合わせ内容",
        }),
    )

    def send_email(self):
        subject = "お問い合わせ"
        message = self.cleaned_data['message']
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        from_email = '{name} <{email}>'.format(name=name, email=email)
        recipient_list = [settings.EMAIL_HOST_USER]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")