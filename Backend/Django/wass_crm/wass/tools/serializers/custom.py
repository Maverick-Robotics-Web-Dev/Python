from decimal import Decimal
from typing import Self
from collections import OrderedDict

from django.db.models import Model
from django.db.models.query import QuerySet

from django.contrib.auth.hashers import make_password

from rest_framework.relations import PKOnlyObject
from rest_framework.fields import SkipField
from rest_framework.serializers import (
    ModelSerializer,
    raise_errors_on_nested_writes
)

from tools.methods.datetime import local_datetime
from tools.methods.decimal import convert_decimal


class NestedCustomSerializer(ModelSerializer):

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def create(self: Self, validated_data: OrderedDict) -> Model:

        model: Model = self.get_model()
        validated_data.update({
            'status': True,
            'create_at': local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        instance: Model = model._default_manager.create(**validated_data)

        return instance

    def update(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({'update_at': local_datetime()})

        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            'status': False,
            'update_at': local_datetime()
        })

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


class MiniCustomSerializer(ModelSerializer):

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def create(self: Self, validated_data: OrderedDict) -> Model:

        model: Model = self.get_model()
        validated_data.update({
            'create_at': local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        instance: Model = model._default_manager.create(**validated_data)

        return instance

    def update(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({'update_at': local_datetime()})

        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def save(self: Self, **kwargs: OrderedDict):

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

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, ('`update()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance


class UserSudoCustomSerializer(ModelSerializer):

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def create(self: Self, validated_data: OrderedDict) -> Model:

        model: Model = self.get_model()
        validated_data.update({
            'password': make_password(validated_data.get('password')),
            'status': True,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'create_at': local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        instance: Model = model._default_manager.create(**validated_data)

        return instance

    def update(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({'update_at': local_datetime()})

        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            'status': False,
            'is_active': False,
            'update_at': local_datetime()
        })

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


class UserEmployeeCustomSerializer(ModelSerializer):

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def create(self: Self, validated_data: OrderedDict) -> Model:

        model: Model = self.get_model()
        validated_data.update({
            'password': make_password(validated_data.get('password')),
            'status': True,
            'is_superuser': False,
            'is_staff': False,
            'is_active': True,
            'create_at': local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        instance: Model = model._default_manager.create(**validated_data)

        return instance

    def update(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({'update_at': local_datetime()})

        raise_errors_on_nested_writes('update', self, validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            'status': False,
            'is_active': False,
            'update_at': local_datetime()
        })

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


class CRelatedSerializer(ModelSerializer):

    __instance_detail: list = []

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def get_model_detail(self: Self) -> Model:

        model_detail: Model = self.Meta.model_detail

        return model_detail

    def get_model_product(self: Self) -> Model:

        model_product: Model = self.Meta.model_product

        return model_product

    def create(self: Self, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": True,
            "create_at": local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        model: Model = self.get_model()
        items: list = validated_data.pop('detail')
        instance: Model = model._default_manager.create(**validated_data)
        model_detail: Model = self.get_model_detail()
        model_product: Model = self.get_model_product()
        # item: OrderedDict = {}

        for item in items:
            item.update({
                "status": True,
                "create_at": local_datetime()
            })
            instance_detail: Model = model_detail._default_manager.create(fk_credit_note=instance, **item)
            instance_product: Model = instance_detail.fk_product
            product_stock: Decimal = instance_product.stock
            detail_quantity: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(product_stock)-convert_decimal(detail_quantity)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()
            self.__instance_detail.append(instance_detail)

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": False,
            "update_at": local_datetime()
        })

        raise_errors_on_nested_writes('delete', self, validated_data)

        model_detail: Model = self.get_model_detail()
        instance_product: Model = self.get_model_product()
        items: QuerySet = model_detail._default_manager.filter(fk_credit_note=instance.id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        for instance_detail in items:

            item: OrderedDict = {
                "status": False,
                "update_at": local_datetime()
            }

            for attr, value in item.items():
                setattr(instance_detail, attr, value)
            instance_detail.save()

            instance_product: Model = instance_detail.fk_product
            stock_before: Decimal = instance_product.stock
            stock_detail: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(stock_before) + convert_decimal(stock_detail)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()

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

        # if self.instance is not None and flag == False:
        #     self.instance = self.update(self.instance, validated_data)
        #     assert self.instance is not None, ('`update()` did not return an object instance.')
        if self.instance is not None:
            self.instance = self.delete(self.instance, validated_data)
            assert self.instance is not None, ('`delete()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance

    def to_representation(self: Self, instance: Model):

        ret = OrderedDict()
        fields = self._readable_fields
        setattr(instance, 'detail', self.__instance_detail)

        for field in fields:
            try:
                attr = field.get_attribute(instance)
            except (SkipField):
                continue

            check_for_none = attr.pk if isinstance(attr, PKOnlyObject) else attr
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attr)

        return ret


class SRelatedSerializer(ModelSerializer):

    __instance_detail: list = []

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def get_model_detail(self: Self) -> Model:

        model_detail: Model = self.Meta.model_detail

        return model_detail

    def get_model_product(self: Self) -> Model:

        model_product: Model = self.Meta.model_product

        return model_product

    def create(self: Self, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": True,
            "create_at": local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        model: Model = self.get_model()
        items: list = validated_data.pop('detail')
        instance: Model = model._default_manager.create(**validated_data)
        model_detail: Model = self.get_model_detail()
        model_product: Model = self.get_model_product()
        # item: OrderedDict = {}

        for item in items:
            item.update({
                "status": True,
                "create_at": local_datetime()
            })
            instance_detail: Model = model_detail._default_manager.create(fk_sale=instance, **item)
            instance_product: Model = instance_detail.fk_product
            product_stock: Decimal = instance_product.stock
            detail_quantity: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(product_stock)-convert_decimal(detail_quantity)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()
            self.__instance_detail.append(instance_detail)

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": False,
            "update_at": local_datetime()
        })

        raise_errors_on_nested_writes('delete', self, validated_data)

        model_detail: Model = self.get_model_detail()
        instance_product: Model = self.get_model_product()
        items: QuerySet = model_detail._default_manager.filter(fk_sale=instance.id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        for instance_detail in items:

            item: OrderedDict = {
                "status": False,
                "update_at": local_datetime()
            }

            for attr, value in item.items():
                setattr(instance_detail, attr, value)
            instance_detail.save()

            instance_product: Model = instance_detail.fk_product
            stock_before: Decimal = instance_product.stock
            stock_detail: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(stock_before) + convert_decimal(stock_detail)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()

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

        # if self.instance is not None and flag == False:
        #     self.instance = self.update(self.instance, validated_data)
        #     assert self.instance is not None, ('`update()` did not return an object instance.')
        if self.instance is not None:
            self.instance = self.delete(self.instance, validated_data)
            assert self.instance is not None, ('`delete()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance

    def to_representation(self: Self, instance: Model):

        ret = OrderedDict()
        fields = self._readable_fields
        setattr(instance, 'detail', self.__instance_detail)

        for field in fields:
            try:
                attr = field.get_attribute(instance)
            except (SkipField):
                continue

            check_for_none = attr.pk if isinstance(attr, PKOnlyObject) else attr
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attr)

        return ret


class IRelatedSerializer(ModelSerializer):

    __instance_detail: list = []

    def get_model(self: Self) -> Model:

        model: Model = self.Meta.model

        return model

    def get_model_detail(self: Self) -> Model:

        model_detail: Model = self.Meta.model_detail

        return model_detail

    def create(self: Self, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": True,
            "create_at": local_datetime()
        })

        raise_errors_on_nested_writes('create', self, validated_data)

        model: Model = self.get_model()
        items: list = validated_data.pop('detail')
        instance: Model = model._default_manager.create(**validated_data)
        model_detail: Model = self.get_model_detail()

        for item in items:
            item.update({
                "status": True,
                "create_at": local_datetime()
            })
            instance_detail: Model = model_detail._default_manager.create(fk_income=instance, **item)
            instance_product: Model = instance_detail.fk_product
            product_stock: Decimal = instance_product.stock
            detail_quantity: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(product_stock) + convert_decimal(detail_quantity)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()
            self.__instance_detail.append(instance_detail)

        return instance

    def delete(self: Self, instance: Model, validated_data: OrderedDict) -> Model:

        validated_data.update({
            "status": False,
            "update_at": local_datetime()
        })

        raise_errors_on_nested_writes('delete', self, validated_data)

        model_detail: Model = self.get_model_detail()
        items: QuerySet = model_detail._default_manager.filter(fk_income=instance.id)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        for instance_detail in items:

            item: OrderedDict = {
                "status": False,
                "update_at": local_datetime()
            }

            for attr, value in item.items():
                setattr(instance_detail, attr, value)
            instance_detail.save()

            instance_product: Model = instance_detail.fk_product
            stock_before: Decimal = instance_product.stock
            stock_detail: Decimal = instance_detail.quantity
            current_stock: Decimal = convert_decimal(stock_before) - convert_decimal(stock_detail)
            setattr(instance_product, 'stock', current_stock)
            instance_product.save()

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

        # if self.instance is not None and flag == False:
        #     self.instance = self.update(self.instance, validated_data)
        #     assert self.instance is not None, ('`update()` did not return an object instance.')
        if self.instance is not None:
            self.instance = self.delete(self.instance, validated_data)
            assert self.instance is not None, ('`delete()` did not return an object instance.')
        else:
            self.instance = self.create(validated_data)
            assert self.instance is not None, ('`create()` did not return an object instance.')

        return self.instance

    def to_representation(self: Self, instance: Model):

        ret = OrderedDict()
        fields = self._readable_fields
        setattr(instance, 'detail', self.__instance_detail)

        for field in fields:
            try:
                attr = field.get_attribute(instance)
            except (SkipField):
                continue

            check_for_none = attr.pk if isinstance(attr, PKOnlyObject) else attr
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attr)

        return ret
