from _collections_abc import dict_items
from collections import OrderedDict


def get_error_message(errors_items: dict_items) -> OrderedDict:

    error_message: OrderedDict = {}
    for attr, errors in errors_items:
        for error in errors:
            error_message.update({attr: error})

    return error_message
