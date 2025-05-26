from django.db.models import (
    Model,
    CharField,
    BooleanField,
    DateTimeField
)


class NestedModel(Model):

    status: BooleanField = BooleanField('Estado', default=True)
    status_description: CharField = CharField('Descripción del Estado', max_length=256, default='No existe descripción')
    create_at: DateTimeField = DateTimeField('Fecha de Creación', null=True, blank=False)
    update_at: DateTimeField = DateTimeField('Fecha de Actualización', null=True, blank=False)

    class Meta:

        abstract: bool = True
