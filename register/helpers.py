from register.models import EmailValidationToken


def create_email_validation_token(user):
    token = EmailValidationToken.objects.create(user=user)
    return str(token.token)
