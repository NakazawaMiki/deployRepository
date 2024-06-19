from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, UsernameChangeForm, CustomPasswordResetForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .forms import CustomSetPasswordForm
from .forms import ContactForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('accounts:signup_success')

    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    template_name = "signup_success.html"

class ChangeUsernameView(LoginRequiredMixin, FormView):
    template_name = "change_username.html"
    form_class = UsernameChangeForm

    def form_valid(self, form):
        new_username = form.cleaned_data['new_username']
        user = self.request.user  
        user.username = new_username
        user.save()
        messages.success(self.request, 'ユーザー名を変更しました。')
        return redirect('accounts:change_username_success')

class ChangeUsernameSuccessView(TemplateView):
    template_name = "change_username_success.html"




class CustomPasswordResetView(FormView):
    template_name = 'password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        CustomUser = get_user_model()
        user = CustomUser.objects.filter(email=email).first()
        if user is not None:
            username = user.username
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = self.request.build_absolute_uri(
                reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            email_body = (
                f'{username} 様\n\n'
                f'パスワードのリセットが要求されました。\n'
                f'以下のリンクをクリックしてパスワードをリセットしてください。\n\n'
                f'{reset_url}'
            )
            send_mail(
                'パスワードのリセット',
                email_body,
                'from@example.com',
                [email],
                fail_silently=False,
            )
        else:
            messages.error(self.request, "登録されていないメールアドレスです。")
            return redirect('password_reset')
        return super().form_valid(form)




class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')



from django.views.generic import FormView, TemplateView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.conf import settings
from .forms import ContactForm

class ContactFormView(FormView):
    template_name = 'contact_form.html'  
    form_class = ContactForm
    success_url = reverse_lazy('accounts:contact_result')

    def form_valid(self, form):
        self.send_email(form.cleaned_data)
        return super().form_valid(form)

    def send_email(self, cleaned_data):
        subject = "お問い合わせ"
        message = cleaned_data['message']
        name = cleaned_data['name']
        email = cleaned_data['email']
        from_email = f'{name} <{email}>'
        recipient_list = [settings.EMAIL_HOST_USER]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse("無効なヘッダが検出されました。")

class ContactResultView(TemplateView):
    template_name = 'contact_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは正常に送信されました。"
        return context
