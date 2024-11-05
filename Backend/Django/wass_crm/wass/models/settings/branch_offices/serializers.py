from django.db.models import Model

from models.settings.branch_offices.models import BranchOfficesModel
from tools.serializers.custom import NestedCustomSerializer


class BranchOfficesSerializer(NestedCustomSerializer):

    class Meta:

        model: Model = BranchOfficesModel
        fields: str | list = '__all__'
