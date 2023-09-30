from django.urls import path
from .views import *

urlpatterns = [
    path('', Events.as_view(), name='events-list'),
    path('<int:event_id>/', EventDetail.as_view(), name='event-detail'),

    path('<int:event_id>/participate/', EventParticipateAPIView.as_view(), name='participate'),
    path('<int:event_id>/cancel-participation/', EventCancelParticipationAPIView.as_view(), name='cancel-participation'),

    path('my-events/', MyEvents.as_view(), name='my-events'),
]