from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer


class Events(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get(self, request):
        """
        Получение записей Event
        """

        page_num = int(request.GET.get('page', 1))
        limit_num = int(request.GET.get('limit', 10))

        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num

        search_param = request.GET.get('search')

        events = Event.objects.all()

        not_user_param = request.GET.get('not_user')

        if not_user_param:
            events = Event.objects.exclude(creator = not_user_param).exclude(participants__id=int(not_user_param))

        if search_param:
            events = events.filter(title__icontains=search_param)

        serializer = self.serializer_class(events[start_num:end_num], many=True)


        return Response({
            "status": "success",
            "page": page_num,
            "events": serializer.data
        })

    def post(self, request):
        """
        Добавление записи Event
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"event": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get_event(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except:
            return None

    def get(self, request, event_id):
        """
        Получение записи Event
        """
        event = self.get_event(event_id)
        if event is None:
            return Response({"status": "fail", "error": f"Event with id: {event_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(event)
        return Response({"status": "success", "data": {"event": serializer.data}})


    def delete(self, request, event_id):
        """
        Удаление записи Event
        """
        event = self.get_event(event_id)
        if event is None:
            return Response({"status": "fail", "error": f"Event with id: {event_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if event.creator == request.user or request.user.is_superuser:
            event.delete()
            return Response({"status": "success", "message": f"Event with id: {event_id} successfully deleted"})

        return Response({'status': 'fail', 'error': 'You are not allowed to delete this event'})

class EventParticipateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if event is None:
            return Response({'status': 'failed', 'error': f'Event with id {event_id} not found'})

        event.participants.add(request.user)
        return Response({'status': 'success', 'result': 'You have participated in the event'})

class EventCancelParticipationAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        if event is None:
            return Response({'status': 'failed', 'error': f'Event with id {event_id} not found'})

        event.participants.remove(request.user)
        return Response({'status': 'success', 'result': 'You have canceled your participation in the event'})
    

class MyEvents(generics.GenericAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def get(self, request):
        my_events = Event.objects.filter(creator=request.user)
        i_participant = Event.objects.filter(participants__id=request.user.id) 
        res = set(my_events | i_participant)

        serializer = self.serializer_class(res, many=True)
        return Response({"status": "success", "data": {"events": serializer.data}})
