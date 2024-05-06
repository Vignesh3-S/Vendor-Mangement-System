from rest_framework import serializers
from .models import Vendor,Purchase_Order,Historical_Performance
import random
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class User_Serializer(serializers.ModelSerializer):
    password = serializers.CharField( write_only=True,required=True,help_text = 'create a strong passsword using alphanumerics and special characters.',
        style={'input_type': 'password', 'placeholder': 'Password','minlength':8,'maxlength':15})
    confirm_password = serializers.CharField( write_only=True,required=True,help_text='same as in the password field.',
        style={'input_type': 'password', 'placeholder': 'Confirm Password','minlength':8,'maxlength':15})
    class Meta:
        model=User
        fields = ('username','email','password','confirm_password',)
    
    def create(self,data):            
        if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError({'message':['Your password and confirm password mis-matched']})
        try:
            validate_password(password=data.get('password'))
        except ValidationError as e:
            raise serializers.ValidationError(list(e))
        data.pop('confirm_password')    
        data['password'] = make_password(data.get('password'))
        return super(User_Serializer,self).create(data)

class Vendor_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
    
    def create(self,data):
        data['vendor_code'] = random.randrange(100000,1000000)
        return super(Vendor_Serializer,self).create(data)
    
class Purchase_Order_Serializer1(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        fields = "__all__"
    
    def to_representation(self,instance):
        data = super(Purchase_Order_Serializer1,self).to_representation(instance)
        data['vendor'] = instance.vendor.name
        data['order_date'] = instance.order_date.strftime("%b %d, %Y at %I:%M %p")
        data['expected_delivery_date'] = instance.expected_delivery_date.strftime("%b %d, %Y at %I:%M %p")
        data['issue_date'] = instance.issue_date.strftime("%b %d, %Y at %I:%M %p")
        if data['acknowledgment_date']:
            data['acknowledgment_date'] = instance.acknowledgment_date.strftime("%b %d, %Y at %I:%M %p")
        return data
            
    def create(self,data):
        data['po_number'] = random.randrange(100000,1000000)
        order = data['order_date']
        expected = data['expected_delivery_date']
        if (expected-order).days * 86400 + (expected-order).seconds < 0:
            raise serializers.ValidationError({'message':['Expected date sholud be after the order date']})
        return super(Purchase_Order_Serializer1,self).create(data)
    
    def update(self,instance,data):
        if data.get('order_date') or data.get('expected_delivery_date'):
            order = data.get('order_date')
            expected = data.get('expected_delivery_date')
            if (expected-order).days * 86400 + (expected-order).seconds < 0:
                raise serializers.ValidationError({'message':['Expected date sholud be after the order date']})
        return super(Purchase_Order_Serializer1,self).update(instance,data)

class Purchase_Order_Serializer2(serializers.ModelSerializer):
    class Meta:
        model = Purchase_Order
        fields = ('acknowledgment_date','po_number','status','issue_date',)
    def update(self,instance,data):
        issue = instance.issue_date
        if data.get('acknowledgment_date'):
            ack = data.get('acknowledgment_date')
            if (ack - issue).days * 86400 + (ack - issue).seconds < 0:
                raise serializers.ValidationError({'message':['Acknowledgement date should be after the issue date']})
        return super(Purchase_Order_Serializer2,self).update(instance,data)
            
class Historical_Performance_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Historical_Performance
        fields = "__all__"
        
    def to_representation(self,instance):
        data = super(Historical_Performance_Serializer,self).to_representation(instance)
        data['vendor'] = instance.vendor.name
        data['date'] = instance.date.strftime("%b %d, %Y at %I:%M %p")
        return data