from django.contrib import admin

from .models import Event, Participant, Organizer, Venue, Rating, Subscription, EventCategory

admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Organizer)
admin.site.register(Venue)
admin.site.register(Rating)
admin.site.register(Subscription)
admin.site.register(EventCategory)
