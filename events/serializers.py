from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg

from .models import Event, Participant, Organizer, Venue, Rating, Subscription, EventCategory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class OrganizerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Organizer
        fields = ['id', 'user', 'company_name']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer(read_only=True)
    venue = VenueSerializer()
    category = EventCategorySerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites.filter(id=user.id).exists()
        return False

    def get_average_rating(self, obj):
        avg_rating = obj.ratings.aggregate(avg=Avg('score'))['avg']
        return avg_rating or 0

    def get_participants_count(self, obj):
        return obj.participants.count()

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
