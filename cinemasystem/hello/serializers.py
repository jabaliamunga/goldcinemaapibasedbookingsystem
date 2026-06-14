from rest_framework import serializers
from .models import Production, Booking, Customer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'




class BookingSerializer(serializers.ModelSerializer):
#for get ie get id s and names based on the foreign key
    customer_email = serializers.EmailField(
        source='customer.email',
        read_only=True
    )

    production_name = serializers.CharField(
        source='production.production_name',
        read_only=True
    )
#for post request
    customer = serializers.SlugRelatedField(
        slug_field='email',
        queryset=Customer.objects.all(),
        write_only=True
    )

    production = serializers.SlugRelatedField(
        slug_field='production_name',
        queryset=Production.objects.all(),
        write_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'customer',
            'production',
            'customer_email',
            'production_name',
            'seat_preference',
            'booked_at'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'password']

    # 🔥 THIS IS THE FIX (VERY IMPORTANT)
    def create(self, validated_data):
        password = validated_data.pop('password')

        customer = Customer.objects.create(
            **validated_data
        )

        # ✅ correct way
        customer.set_password(password)
        customer.save()
        return customer
    
#for our jwt auth to use email for login


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'    
#serialisers convert models to json and json back to python objects


