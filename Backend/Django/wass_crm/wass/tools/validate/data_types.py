from decimal import Decimal
from typing import Any
from django.db.models import Model, DecimalField
from collections import OrderedDict

from tools.methods.decimal import convert_decimal


def validated_data_types(model: Model, validated_data: OrderedDict) -> OrderedDict:

    for mdl_base in model.__bases__:
        for attr, value in mdl_base.__annotations__.items():

            if value == DecimalField:
                attr_value: Any | None = validated_data.get(attr)

                if attr_value is not None:
                    attr_convert: Decimal = convert_decimal(attr_value)
                    validated_data[attr] = attr_convert

    for attr, value in model.__annotations__.items():

        if value == DecimalField:
            attr_value: Any | None = validated_data.get(attr)

            if attr_value is not None:
                attr_convert: Decimal = convert_decimal(attr_value)
                validated_data[attr] = attr_convert

    return validated_data


# def validated_data_types(model: Model, validated_data: OrderedDict) -> OrderedDict:

#     for mdl_base in model.__bases__:
#         for attr, value in mdl_base.__annotations__.items():

#             if value == DateTimeField:
#                 attr_value: Any | None = validated_data.get(attr)

#                 if attr_value is not None:
#                     attr_convert: datetime | Decimal = convert_datetime(attr_value)
#                     validated_data[attr] = attr_convert

#             if value == DecimalField:
#                 attr_value: Any | None = validated_data.get(attr)

#                 if attr_value is not None:
#                     attr_convert: datetime | Decimal = convert_decimal(attr_value)
#                     validated_data[attr] = attr_convert

#     for attr, value in model.__annotations__.items():

#         if value == DateTimeField:
#             attr_value: Any | None = validated_data.get(attr)

#             if attr_value is not None:
#                 attr_convert: datetime | Decimal = convert_datetime(attr_value)
#                 validated_data[attr] = attr_convert

#         if value == DecimalField:
#             attr_value: Any | None = validated_data.get(attr)

#             if attr_value is not None:
#                 attr_convert: datetime | Decimal = convert_decimal(attr_value)
#                 validated_data[attr] = attr_convert

#     return validated_data
