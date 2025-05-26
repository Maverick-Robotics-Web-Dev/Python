from rest_framework.serializers import (Serializer, EmailField, CharField)


class AuthSerializer(Serializer):
    email: EmailField = EmailField()
    password: CharField = CharField(max_length=256)
