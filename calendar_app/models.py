from django.db import models
from accounts.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    duration_days = models.PositiveIntegerField(default=1)
    duration_hours = models.PositiveIntegerField(default=0)
    recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(max_length=20, blank=True, null=True)
    recurrence_end_date = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return self.title
