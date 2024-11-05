from django.db.models import (
    Model,
    DateTimeField
)


class MiniModel(Model):

    create_at: DateTimeField = DateTimeField('Fecha de Creación', blank=True, null=True)
    update_at: DateTimeField = DateTimeField('Fecha de Actualización', blank=True, null=True)

    class Meta:

        abstract: bool = True
