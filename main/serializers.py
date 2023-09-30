from rest_framework import serializers
from .models import *


class EventSerializer(serializers.ModelSerializer):
    """
    Сериалайзер модели Event
    """
    class Meta:
        model = Event
        fields = ('id', 'title', 'text', 'creation_date', 'creator', 'participants')