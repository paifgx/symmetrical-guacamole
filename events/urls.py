from rest_framework import routers
from django.urls import path, include

from .views import (
    EventViewSet, ParticipantViewSet, OrganizerViewSet,
    VenueViewSet, RatingViewSet,
    StatisticsView, OrganizerEventViewSet,
    SubscriptionViewSet, EventCategoryViewSet
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'organizers', OrganizerViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'organizer-events', OrganizerEventViewSet, basename='organizer-events')
router.register(r'categories', EventCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
