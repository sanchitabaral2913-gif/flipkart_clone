from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone

class Event(models.Model):
    STATUS_CHOICES = (
        ('Pending','Pending'),
        ('Accepted','Accepted'),
        ('Rejected','Rejected'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_hours = models.IntegerField(default=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def end_time(self):
        start = datetime.combine(self.date, self.start_time)
        return (start + timedelta(hours=self.duration_hours)).time()

    def __str__(self):
        return f"{self.title} by {self.created_by.username}"

    class Meta:
        ordering = ['date', 'start_time']  # fix order in admin & views
