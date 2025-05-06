from typing import Self
from collections import OrderedDict

from django.db.models import Model

from rest_framework.serializers import (ModelSerializer, raise_errors_on_nested_writes)
from rest_framework.utils import model_meta


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

    def update(self: Self, instance: Model, validated_data: OrderedDict) -> Model:
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:
        validated_data.update({'status': False})
        raise_errors_on_nested_writes('delete', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def save(self: Self, flag: bool = False, **kwargs: OrderedDict):

        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None and flag == False:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, ('`update()` did not return an object instance.')
        elif self.instance is not None and flag == True:
            self.instance = self.delete(self.instance, validated_data)
            assert self.instance is not None, ('`delete()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance
