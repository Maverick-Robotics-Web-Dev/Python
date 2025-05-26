from typing import Self, LiteralString
from django.db.models import (Model, AutoField, ForeignKey, CharField, EmailField, ImageField, ManyToManyField, CASCADE)

from models.abstract.nested_model import NestedModel


class UserHasRolesModel(Model):
    id_user: ForeignKey = ForeignKey(to='users.UserModel', on_delete=CASCADE, db_column='id_user')
    id_role: ForeignKey = ForeignKey(to='roles.RoleModel', on_delete=CASCADE, db_column='id_role')

    class Meta:
        db_table = 'USER_HAS_ROLES'
        unique_together = ('id_user', 'id_role')


class UserModel(NestedModel):
    id: AutoField = AutoField(verbose_name='ID', primary_key=True)
    name: CharField = CharField(verbose_name='Nombre', max_length=256)
    lastname: CharField = CharField(verbose_name='Apellido', max_length=256)
    email: EmailField = EmailField(verbose_name='Email', unique=True)
    phone: CharField = CharField(verbose_name='Teléfono', max_length=20)
    image: ImageField = ImageField('Imagen', upload_to='users/', default='default.jpg')
    password: CharField = CharField(verbose_name='Contraseña', max_length=256)
    notification_token: CharField = CharField(verbose_name='Token de Notificación', max_length=256, null=True)
    role = ManyToManyField('roles.RoleModel', through='users.UserHasRolesModel', related_name='USERS')

    class Meta:

        db_table: str = 'USERS'
        verbose_name: str = 'USER'
        verbose_name_plural: str = 'USERS'

    def __str__(self: Self) -> LiteralString:

        mdl_attr: str = str(object=self.name)

        return mdl_attr
