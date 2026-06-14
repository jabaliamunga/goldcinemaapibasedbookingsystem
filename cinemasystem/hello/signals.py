# hello/signals.py
from django.db.models.signals import post_save
#Imports the post_save signal from Django. This signal is sent after a model’s save() method finishes. 
# We use it to run code automatically whenever a Production is created or updated.
from django.dispatch import receiver
#Imports the receiver decorator, a convenient way to register a function as a handler for a signal.
from django.core.mail import send_mail
#Imports Django’s simple email helper. send_mail sends an email using the email backend configurations in settings.py.
from .models import Production, Customer
#here we import the Production model (to monitor new productions) and the Customer model (to get client emails).

@receiver(post_save, sender=Production)
#this means run this function only when the production has been saved (created or updated).
def notify_clients_on_new_production(sender, instance, created, **kwargs):
    """sender: the model class that sent the signal (here, Production).

       instance: the actual Production instance that was saved. You can inspect its fields (e.g., instance.production_name).

        created: a boolean that is True if this save created a new object, False if an existing object was updated.

         **kwargs: extra info Django may pass (ignored here)."""
    if created:  # only send when new production is added
        subject = f"🎬 New {instance.production_type} Added: {instance.production_name}"
        message = (
            f"Hello!\n\n"
            f"We’ve added a new {instance.production_type} — {instance.production_name}.\n"
            f"It will be showing on {instance.start_date}.\n\n"
            f"Book your seat now at Gold Cinema!\n\n"
            f"Best regards,\nGold Cinema Team"
        )

        # Send to all registered client emails
        recipients = list(Customer.objects.values_list('email', flat=True))
        if recipients:
            for email in recipients:
                send_mail(
                    subject,
                    message,
                    'GOLD CINEMA COMPANY <jabaliamunga@gmail.com>',
                    [email],  # ✅ wrap each one in a list
                    fail_silently=False,
            )

