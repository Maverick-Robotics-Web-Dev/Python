from apps.roles.models import RoleModel
from customs.serializers.model_custom_serializer import ModelCustomSerializer


class RoleSerializer(ModelCustomSerializer):
    class Meta:
        model: RoleModel = RoleModel
        fields: str | list = '__all__'
        extra_kwargs = {
            'status': {'write_only': True},
            'status_description': {'write_only': True},
            'create_at': {'write_only': True},
            'update_at': {'write_only': True}
        }
