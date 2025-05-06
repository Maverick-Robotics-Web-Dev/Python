from django.db.models import Model

from models.users.models import UserModel
from customs.serializers.custom_serializer import CustomModelSerializer


class UserSerializer(CustomModelSerializer):
    class Meta:
        model: Model = UserModel
        fields: str | list = '__all__'
