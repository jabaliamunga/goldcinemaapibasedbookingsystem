from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Production, Booking, Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    ordering = ['email']
    list_display = ['customer_code', 'email', 'first_name', 'last_name', 'phone', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address', 'customer_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'address', 'password1', 'password2'),
        }),
    )

    readonly_fields = ['customer_code']


admin.site.register(Production)
admin.site.register(Booking)