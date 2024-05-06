from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Vendor,Purchase_Order,Historical_Performance
from .serializers import (Vendor_Serializer,Purchase_Order_Serializer1,
                          Purchase_Order_Serializer2,Historical_Performance_Serializer,User_Serializer)
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime,timezone
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny

class CreateUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = User_Serializer
    
class Vendors(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = Vendor_Serializer
    pagination_class = PageNumberPagination
    
class VendorsDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = Vendor_Serializer
    lookup_field = 'vendor_code'
    lookup_url_kwarg = 'vendor_code'

class Purchase_Orders(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_Order_Serializer1
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vendor']
    pagination_class = PageNumberPagination

class Update_Purchase_Order(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_Order_Serializer1
    lookup_field = 'po_number'
    lookup_url_kwarg = 'po_number'
    
class Performance_History(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,vendor_code,format=None):
        try:
            vendor = Vendor.objects.get(vendor_code = vendor_code)
            get_vendor_id = vendor.id
            vendor_history = Historical_Performance.objects.get(vendor = get_vendor_id)
        except:
            raise Http404
        serializer = Historical_Performance_Serializer(vendor_history)
        return Response(serializer.data,status=status.HTTP_200_OK)

class Vendor_Acknowledgement(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Purchase_Order.objects.all()
    serializer_class = Purchase_Order_Serializer2
    lookup_field = 'po_number'
    lookup_url_kwarg = 'po_number'

@receiver(post_save,sender=Vendor)
def create_history_performance(sender,instance,**kwargs):
    vendor=Historical_Performance.objects.get_or_create(vendor=instance)
    
@receiver(post_save,sender=Purchase_Order)
def update_performance_metrics(sender,instance,**kwargs):
    order = Purchase_Order.objects.get(po_number = instance.po_number)
    # on time delivery rate
    if order.status == 'Completed':
        vendor_orders= Purchase_Order.objects.filter(vendor=instance.vendor,status='Completed')
        in_time_count = 0
        for i in vendor_orders:
            if ((datetime.now() - i.expected_delivery_date).days)*86400 + \
            (datetime.now() - i.expected_delivery_date).seconds == 0  or \
            (((datetime.now() - i.expected_delivery_date).days)*86400 + \
            (datetime.now() - i.expected_delivery_date).seconds) < 0:
                in_time_count += 1
        try:
            get_vendor = Vendor.objects.get(id=order.vendor.id)
            get_vendor.on_time_delivery_rate = in_time_count / len(vendor_orders)
            get_vendor.save()
            vendor_history = Historical_Performance.objects.get(vendor=order.vendor)
            vendor_history.on_time_delivery_rate = get_vendor.on_time_delivery_rate
            vendor_history.save()
        except:
            pass
    # quality rating average
    if order.quality_rating:
        vendor_orders = Purchase_Order.objects.filter(vendor=instance.vendor,status='Completed')
        ratings =  0
        for i in vendor_orders:
            if i.quality_rating != None:
                ratings += i.quality_rating
        try:
            get_vendor = Vendor.objects.get(id=order.vendor.id)
            get_vendor.quality_rating_avg = ratings / len(vendor_orders)
            get_vendor.save()
            vendor_history = Historical_Performance.objects.get(vendor=order.vendor)
            vendor_history.quality_rating_avg = get_vendor.quality_rating_avg
            vendor_history.save()
        except:
            pass
    # Average response time
    if order.acknowledgment_date:
        vendor_orders = Purchase_Order.objects.filter(vendor=instance.vendor)
        date_difference =  0
        for i in vendor_orders:
            if i.acknowledgment_date:
                date_difference += ((i.acknowledgment_date-i.issue_date).days) * 86400 + (i.acknowledgment_date-i.issue_date).seconds
        try:
            get_vendor = Vendor.objects.get(id=order.vendor.id)
            get_vendor.average_response_time = date_difference / len(vendor_orders)
            get_vendor.save()
            vendor_history = Historical_Performance.objects.get(vendor=order.vendor)
            vendor_history.average_response_time = get_vendor.average_response_time
            vendor_history.save()
        except:
            pass
    #fulfilment rate
    if order.status == 'Completed':
        vendor_orders= Purchase_Order.objects.filter(vendor=instance.vendor)
        vendor_completed_orders = Purchase_Order.objects.filter(vendor=instance.vendor,status='Completed')
        try:
            get_vendor = Vendor.objects.get(id=order.vendor.id)
            get_vendor.fulfillment_rate = len(vendor_completed_orders) / len(vendor_orders)
            get_vendor.save()
            vendor_history = Historical_Performance.objects.get(vendor=order.vendor)
            vendor_history.fulfillment_rate =  get_vendor.fulfillment_rate
            vendor_history.save()
        except:
            pass
    return
    
