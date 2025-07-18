from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import Task

# Reminder is sent upon creation of a task that expires in an hour or less
# For a reminder to be sent automatically, a background scheduler like cron tabs is necessary
@receiver(post_save, sender=Task)
def send_task_reminder(sender, instance, created, **kwargs):
    if not created:
        return

    now = timezone.now()
    due_soon = now + timedelta(hours=1)
    if not instance.is_complete and instance.due_date <= due_soon and instance.due_date >= now:
        send_mail(
            subject=f"Task Reminder: '{instance.title}' is due soon",
            message=f"Hi there, this is a reminder that your task '{instance.title}' is due at {instance.due_date}.",
            from_email="no-reply@todoapp.com",
            recipient_list=[instance.user.email],
            fail_silently=True,  # so local testing doesn't crash
        )