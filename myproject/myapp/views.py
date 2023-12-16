from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Person, Order, OrderItem
from .serializers import PersonSerializer, OrderSerializer
from django.shortcuts import get_object_or_404

# views.py

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to my project!")


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'order_id': serializer.data['order_id']}, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['POST'])
def add_order_items(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()
        return Response({'order_id': order.order_id, 'order_part_seq_id': order.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    response_data = {'orders': serializer.data}
    return Response(response_data)

@api_view(['GET'])
def get_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['PUT'])
def update_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    serializer = OrderSerializer(instance=order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=400)
