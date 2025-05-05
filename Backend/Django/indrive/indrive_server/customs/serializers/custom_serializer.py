from typing import Self
from collections import OrderedDict

from django.db.models import Model

from rest_framework.serializers import (ModelSerializer, raise_errors_on_nested_writes)


class CustomModelSerializer(ModelSerializer):

    def get_model(self: Self) -> Model:
        model: Model = self.Meta.model
        return model

    def create(self: Self, validated_data: OrderedDict) -> Model:
        model: Model = self.get_model()
        validated_data.update({'status': True})
        raise_errors_on_nested_writes('create', self, validated_data)
        instance: Model = model._default_manager.create(**validated_data)

        return instance
