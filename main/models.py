from django.db import models

from authentication.models import CustomUser


class Event(models.Model):
    """
    Модель Событие
    """
    title = models.TextField(max_length=100)
    text = models.TextField(max_length=1500)
    creation_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(CustomUser, related_name='created_events', on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(CustomUser, related_name='participated_events', null=True, blank=True)

    def __str__(self):
        return self.title