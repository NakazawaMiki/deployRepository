
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ContactFormView, ContactResultView

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('change_username/', views.ChangeUsernameView.as_view(), name='change_username'),
    path('change_username_success/', views.ChangeUsernameSuccessView.as_view(), name='change_username_success'),
    path('contact/', views.ContactFormView.as_view(), name='contact_form'),
    path('contact/result/', views.ContactResultView.as_view(), name='contact_result'),
]






