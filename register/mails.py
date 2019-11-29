from templated_email import send_templated_mail


def send_email_validation_email(request, user, token, account_created=True):
    send_templated_mail(
        template_name='account_created' if account_created else 'validate_email',
        from_email='formmaker667@gmail.com',
        recipient_list=[user.email],
        context={
            'user': user,
            'url': str(request.get_host() + '/register/confirm_email/' + token + '/')
        }
    )
