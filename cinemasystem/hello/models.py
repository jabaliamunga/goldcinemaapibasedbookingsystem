from django.db import models
from django.utils import timezone

class Production(models.Model):
    PRODUCTION_TYPES = [
        ('concert', 'Concert'),
        ('play', 'Play'),
        ('movie', 'Movie'),
    ]

    production_name = models.CharField(max_length=100)
    production_type = models.CharField(max_length=20, choices=PRODUCTION_TYPES)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    production_show_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.production_name} ({self.get_production_type_display()}) {self.start_date}"
    
from django.db import models

class Customer(models.Model):
    customer_code = models.BigIntegerField(unique=True, editable=False)

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        # If new customer, generate code
        if not self.customer_code:
            last_customer = Customer.objects.order_by('-customer_code').first()

            if last_customer:
                self.customer_code = last_customer.customer_code + 1
            else:
                self.customer_code = 45601  # starting point

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_code} - {self.first_name} {self.last_name}"


class Booking(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE)
    production = models.ForeignKey("Production", on_delete=models.CASCADE)

    booked_at = models.DateTimeField(auto_now_add=True)
    seat_preference = models.IntegerField()

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # ✅ Use production_type from related model
        if self.production.production_type == "movie":
            self.amount = 300
        elif self.production.production_type == "play":
            self.amount = 400
        elif self.production.production_type == "concert":
            self.amount = 600
        else:
            self.amount = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.customer.email} ({self.production.production_name}) - {self.amount} KES"

    
    


# Create your models here.
