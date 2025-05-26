from django.db.models import Model
from django.shortcuts import get_object_or_404

from rest_framework.serializers import ModelSerializer
from rest_framework.utils import model_meta


def create_many_to_many_relation(model_to_get: Model, many_to_many_model: Model, model_created: Model, serializer_model_to_get: ModelSerializer, id_model_get: any,  column_name: any, col_name: any):
    """
    This is the same as below but in a dynamic way:

    client_role = get_object_or_404(RoleModel, id='CLIENT')
    UserHasRolesModel._default_manager.create(id_user=user, id_role=client_role)
    roles = RoleModel._default_manager.filter(userhasrolesmodel__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)
    """
    get_model = get_object_or_404(model_to_get, id=id_model_get)
    relational_fields = {
        f'{column_name}': model_created,
        f'{col_name}': get_model
    }
    name_model_lower = {
        f'{str(many_to_many_model.__name__).lower()}__{column_name}': model_created
    }

    many_to_many_model._default_manager.create(**relational_fields)
    get_by_id_model = model_to_get._default_manager.filter(**name_model_lower)
    roles_serializer: ModelSerializer = serializer_model_to_get(get_by_id_model, many=True)

    return roles_serializer.data
