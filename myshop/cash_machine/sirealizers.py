from rest_framework.serializers import ModelSerializer, Serializer, ListField, IntegerField
from cash_machine.models import Item


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "price",
        ]


class CashMachineSerializer(Serializer):
    items = ListField(child=IntegerField())