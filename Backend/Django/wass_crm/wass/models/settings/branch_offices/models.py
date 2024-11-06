from typing import Self, LiteralString

from django.db.models import (AutoField, ForeignKey, CharField, ImageField, CASCADE)

from models.abstract.nested import NestedModel


class BranchOfficesModel(NestedModel):

    id: AutoField = AutoField('ID', primary_key=True)
    name: CharField = CharField('Nombre', unique=True, max_length=250)
    country: CharField = CharField('Pais', max_length=200)
    state_province: CharField = CharField('Provincia o Estado', max_length=200)
    city: CharField = CharField('Ciudad', max_length=200)
    address: CharField = CharField('Dirección', max_length=200)
    postal_code: CharField = CharField('Codigo Postal', max_length=200, default='S/N')
    cellphone_number: CharField = CharField('Celular', max_length=50)
    phone_number: CharField = CharField('Telefono', max_length=50, default='Sin Telefono Convencional')
    email: CharField = CharField('E-mail', max_length=100, default='No Posee email')
    img: ImageField = ImageField('Imagen', upload_to='persons/', blank=True, null=True)
    # fk_user_employee: ForeignKey = ForeignKey('user_employee.UserEmployeeModel', on_delete=CASCADE, verbose_name='Usuario')

    class Meta:

        db_table: str = 'APP_BRANCH_OFFICES'
        verbose_name: str = 'BRANCH_OFFICE'
        verbose_name_plural: str = 'BRANCH_OFFICES'

    def __str__(self: Self) -> LiteralString:

        mdl_attr: str = str(self.name)

        return mdl_attr
