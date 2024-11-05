from django.db.models import (
    Model,
    CharField,
    ImageField,
)


class NestedSupplierModel(Model):

    document_type: CharField = CharField('Tipo de Documento', max_length=20)
    document_number: CharField = CharField('Numero', max_length=20)
    country: CharField = CharField('Pais', max_length=200)
    state_province: CharField = CharField('Provincia o Estado', max_length=200)
    city: CharField = CharField('Ciudad', max_length=200)
    address: CharField = CharField('Dirección', max_length=200)
    postal_code: CharField = CharField('Codigo Postal', max_length=200, default='S/N')
    phone_number: CharField = CharField('Telefono', max_length=50, default='Sin Telefono Convencional')
    cellphone_number: CharField = CharField('Celular', max_length=50)
    email: CharField = CharField('E-mail', max_length=100, default='No Posee email')
    img: ImageField = ImageField('Imagen', upload_to='supplierss/', blank=True, null=True)

    class Meta:

        abstract: bool = True
