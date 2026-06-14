from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = None  # remove username since we login with email
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    customer_code = models.BigIntegerField(unique=True, editable=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomerManager()  # ✅ required when USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        if not self.customer_code:
            last_customer = Customer.objects.order_by('-customer_code').first()
            self.customer_code = (last_customer.customer_code + 1) if last_customer else 45601
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_code} - {self.first_name} {self.last_name}"

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
