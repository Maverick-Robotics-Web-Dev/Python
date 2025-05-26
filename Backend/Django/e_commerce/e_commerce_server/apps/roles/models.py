from typing import Self, LiteralString
from django.db.models import CharField

from models.abstract.nested_model import NestedModel


class RoleModel(NestedModel):
    id: CharField = CharField(verbose_name='ID', primary_key=True, max_length=36, editable=True)
    name: CharField = CharField(verbose_name='Nombre', max_length=36)
    image: CharField = CharField(verbose_name='Imagen', max_length=256)
    route: CharField = CharField(verbose_name='Ruta', max_length=256)

    class Meta:

        db_table: str = 'ROLES'
        verbose_name: str = 'ROLE'
        verbose_name_plural: str = 'ROLES'

    def __str__(self: Self) -> LiteralString:

        mdl_attr: str = str(object=self.name)

        return mdl_attr
