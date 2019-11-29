from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render
import logging

from register.helpers import create_email_validation_token
from register.mails import send_email_validation_email
from register.models import EmailValidationToken, Profile

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':

        user = User.objects.filter(username=request.POST['username']).first()
        if user is not None:
            return render(request, 'register/register.html', {
                'message': 'This username is already taken'
            })

        try:
            validate_email(request.POST['email'])
        except ValidationError:
            return render(request, 'register/register.html', {
                'message': 'This email is not valid'
            })

        if len(request.POST['password']) < 8:
            return render(request, 'register/register.html', {
                'message': 'Password must be at least 8 characters'
            })

        if request.POST['password'] != request.POST['password_confirm']:
            return render(request, 'register/register.html', {
                'message': 'Passwords are different'
            })

        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        Profile.objects.create(user=user)

        try:
            token = create_email_validation_token(user)
            send_email_validation_email(request, user, token)
        except Exception as e:
            logger.exception(e)
            user.delete()
            return render(request, 'register/register.html', {
                'message': 'Email sending failed.'
            })

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        auth.login(request, user)

        return render(request, 'main/index.html', {
            'message': 'Your account has been successfully created.'
        })
    return render(request, 'register/register.html')


@login_required
def profile(request):
    return render(request, 'register/profile.html')


def confirm_email(request, uuid):
    token = EmailValidationToken.objects.filter(token=uuid).first()
    if token is not None:
        if token.used:
            return render(request, 'register/message.html', {
                'message': 'Error: This url was already used.',
                'type': 'danger'
            })
        user_profile = token.user.profile
        user_profile.email_confirmed = True
        user_profile.save()
        token.used = True
        token.save()
        return render(request, 'register/message.html', {
            'message': 'Your email has been confirmed.'
        })
    return render(request, 'register/message.html', {
        'message': 'This token could not be found.'
    })


@login_required
def resend_confirm_email(request):
    try:
        token = create_email_validation_token(request.user)
        send_email_validation_email(request, request.user, token, account_created=False)
    except Exception as e:
        logger.exception(e)
        return render(request, 'register/register.html', {
            'message': 'Email sending failed.'
        })
    return render(request, 'register/message.html', {
        'message': 'A new email has been sent.'
    })
