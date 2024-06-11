from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


def generate_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key
