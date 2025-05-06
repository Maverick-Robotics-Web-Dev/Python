from typing import Self
from collections import OrderedDict

from rest_framework.viewsets import GenericViewSet


class CustomViewSet(GenericViewSet):
    action: str = ''
    serializers: OrderedDict = {"default": None}

    def get_serializer_class(self: Self):
        """
        Devuelve un serializador en función del verbo HTTP
        (o acción). Si no está definido, devuelve el serializador
        por defecto.
        """

        return self.serializers.get(
            self.action, self.serializers["default"])

    def get_serializer(self: Self, *args: tuple, **kwargs: dict):
        """
        Devuelve la instancia del serializador que debe usarse para validar y
        deserializar la entrada, y para serializar la salida.
        """

        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
