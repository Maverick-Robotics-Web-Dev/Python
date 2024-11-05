from django.db.models import (
    Model,
    CharField,
    BooleanField,
    DateTimeField
)


class NestedModel(Model):

    status: BooleanField = BooleanField('Estado', default=False)
    status_description: CharField = CharField('Descripción del Estado', max_length=256, default='No existe descripción')
    create_at: DateTimeField = DateTimeField('Fecha de Creación', blank=True, null=True)
    update_at: DateTimeField = DateTimeField('Fecha de Actualización', blank=True, null=True)

    class Meta:

        abstract: bool = True
