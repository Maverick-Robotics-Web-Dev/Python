from django.db.models import Model
from django.shortcuts import get_object_or_404

from rest_framework.serializers import ModelSerializer


def get_user_role(model: Model, id_model: any, serializer_model: ModelSerializer, obj_model: Model, foreign_key_field_name: any, foreign_key_field_nam: any, foreign_model: any):
    get_model = get_object_or_404(model, id=id_model)
    relational_fields = {}
    relational_fields.update({
        foreign_key_field_name: foreign_model,
        foreign_key_field_nam: get_model
    })
    obj_model._default_manager.create(relational_fields)
    get_by_id_model = model._default_manager.filter(name_model_lower__id_user=foreign_model)
    roles_serializer: ModelSerializer = serializer_model(get_by_id_model, many=True)

    return roles_serializer.data
