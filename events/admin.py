from django.contrib import admin
from .models import (
    User,
    Organizer,
    EventCategory,
    Event,
    EventParticipant
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "gender", "birth_date", "is_staff")
    list_filter = ("gender", "is_staff")
    search_fields = ("username", "email")


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ("name", "website")
    search_fields = ("name",)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class EventParticipantInline(admin.TabularInline):
    model = EventParticipant
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_datetime",
        "location",
        "participants_count",
        "adults_only",
    )

    list_filter = (
        "adults_only",
        "categories",
        "start_datetime",
    )

    search_fields = ("title", "description", "location")
    filter_horizontal = ("categories",)

    inlines = [EventParticipantInline]


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "registered_at")
    list_filter = ("status", "registered_at")
    search_fields = ("event__title", "user__username")