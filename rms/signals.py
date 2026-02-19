from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail

@receiver(post_save, sender=Order)
def get_notified(sender, instance, created, **kwargs):
   print("New Order Created.")
   send_mail(
      "Order Created",
      "New order created",
      "a@gmail.com",
      ["x@gmail.com","y@gmail.com"]
   )
   print("mail sent successfully")