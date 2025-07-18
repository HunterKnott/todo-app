from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TaskManager(models.Manager):
    def overdue(self, user):
        now = timezone.now()
        return self.filter(user=user, is_complete=False, due_date__lt=now)

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    is_complete = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')

    objects = TaskManager()

    def __str__(self):
        return self.title
    
    @property
    def is_overdue(self):
        return not self.is_complete and self.due_date < timezone.now()