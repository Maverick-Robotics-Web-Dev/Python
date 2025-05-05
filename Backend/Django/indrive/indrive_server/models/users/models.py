from typing import Self, LiteralString
from django.db.models import (AutoField, CharField, EmailField)

from models.abstract.nested_model import NestedModel


class User(NestedModel):
    id: AutoField = AutoField(verbose_name='ID', primary_key=True)
    name: CharField = CharField(verbose_name='Nombre', max_length=256)
    lastname: CharField = CharField(verbose_name='Apellido', max_length=256)
    email: EmailField = EmailField(verbose_name='Email', unique=True)
    phone: CharField = CharField(verbose_name='Teléfono', max_length=20)
    image: CharField = CharField(verbose_name='Imagen', max_length=256, null=True, blank=False)
    password: CharField = CharField(verbose_name='Contraseña', max_length=256)
    notification_token: CharField = CharField(verbose_name='Token de Notificación', max_length=256, null=True)

    class Meta:

        db_table: str = 'USERS'
        verbose_name: str = 'USER'
        verbose_name_plural: str = 'USERS'

    def __str__(self: Self) -> LiteralString:

        mdl_attr: str = str(self.name)

        return mdl_attr
