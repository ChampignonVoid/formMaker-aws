from django.urls import path
from register.views import register, profile, confirm_email, resend_confirm_email

urlpatterns = [
    path('register', register, name='register'),
    path('profile', profile, name='profile'),
    path('confirm_email/<uuid:uuid>/', confirm_email, name='confirm_email'),
    path('resend_confirm_email/', resend_confirm_email, name='resend_confirm_email')
]
