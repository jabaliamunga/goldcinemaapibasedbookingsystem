from rest_framework import serializers
from .models import Production, Booking, Customer

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    production_name = serializers.CharField(
        source='production.production_name',
        read_only=True
    ) #production_name not in the booking model but has also been included 
    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    ) #not in the bbooking model but also included

    class Meta:
        model = Booking
        fields = '__all__'   


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'password']
        #password will be included in the api but hashed
#serialisers convert models to json and json back to python objects


