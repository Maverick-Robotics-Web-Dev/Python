from rest_framework.serializers import (Serializer, EmailField, CharField)

from apps.users.models import UserModel


class AuthSerializer(Serializer):
    email: EmailField = EmailField()
    password: CharField = CharField(max_length=256)
