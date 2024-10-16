from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg, Sum
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event, Participant, Organizer, Venue, Rating, Subscription, EventCategory
from .serializers import (
    EventSerializer, ParticipantSerializer, OrganizerSerializer, VenueSerializer,
    RatingSerializer, SubscriptionSerializer, EventCategorySerializer
)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category__name', 'venue__name', 'date']
    search_fields = ['title', 'description', 'category__name', 'venue__name']
    ordering_fields = ['date', 'price']

    def perform_create(self, serializer):
        organizer = Organizer.objects.get(user=self.request.user)
        serializer.save(organizer=organizer)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        event = self.get_object()
        event.favorites.add(request.user)
        return Response({'status': 'added to favorites'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        event = self.get_object()
        event.favorites.remove(request.user)
        return Response({'status': 'removed from favorites'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        event = self.get_object()
        Subscription.objects.get_or_create(user=request.user, event=event)
        return Response({'status': 'subscribed to event notifications'}, status=status.HTTP_200_OK)

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.request.data.get('event_id')
        event = Event.objects.get(id=event_id)
        if Participant.objects.filter(event=event, user=self.request.user).exists():
            raise serializers.ValidationError("You are already registered for this event.")
        if event.participants.count() >= event.max_participants:
            raise serializers.ValidationError("This event is full.")
        serializer.save(user=self.request.user, event=event)

class OrganizerViewSet(viewsets.ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    permission_classes = [IsAdminUser]

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminUser]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = serializer.validated_data['event']
        if not Participant.objects.filter(event=event, user=self.request.user).exists():
            raise serializers.ValidationError("You can only rate events you have participated in.")
        if Rating.objects.filter(event=event, user=self.request.user).exists():
            raise serializers.ValidationError("You have already rated this event.")
        serializer.save(user=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

class StatisticsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_events = Event.objects.count()
        total_participants = Participant.objects.count()
        total_revenue = Event.objects.aggregate(total=Sum('price'))['total']
        data = {
            'total_events': total_events,
            'total_participants': total_participants,
            'total_revenue': total_revenue,
        }
        return Response(data)

class OrganizerEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        organizer = Organizer.objects.get(user=self.request.user)
        return Event.objects.filter(organizer=organizer)

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
