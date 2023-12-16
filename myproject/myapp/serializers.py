# serializers.py

from rest_framework import serializers
from .models import Person, Order, OrderItem

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_id', 'item_description', 'quantity', 'unit_amount']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    customer_details = serializers.SerializerMethodField()
    credit_card = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'order_name', 'currency_uom_id', 'sales_channel_enum_id', 'status_id', 'product_store_id', 'placed_date', 'approved_date', 'credit_card', 'customer_details', 'order_items']
        #fields = ['order_id', 'part_name', 'facility_id', 'shipment_method', 'customer_party', 'order_items', 'order_name', 'currency_uom_id', 'sales_channel_enum_id', 'status_id', 'placed_date', 'grand_total', 'customer_details', 'credit_card']

    def get_customer_details(self, obj):
        customer_party = obj.customer_party
        return {
            'customerPartyId': customer_party.partyId,
            'firstName': customer_party.firstName,
            'middleName': customer_party.middleName,
            'lastName': customer_party.lastName
        }

    def get_credit_card(self, obj):
        return obj.get_credit_card()
