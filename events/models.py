from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# -------------------------------
# Użytkownik
# -------------------------------
class User(AbstractUser):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def __str__(self):
        return self.username

# -------------------------------
# Organizator
# -------------------------------
class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

# -------------------------------
# Kategorie wydarzeń
# -------------------------------
class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# -------------------------------
# Wydarzenie
# -------------------------------
class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)

    max_participants = models.IntegerField(null=True, blank=True)
    participants_count = models.IntegerField(default=0)
    adults_only = models.BooleanField(default=False)

    created_by_user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name="created_events"
    )
    created_by_org = models.ForeignKey(
        Organizer, null=True, blank=True, on_delete=models.CASCADE, related_name="created_events"
    )

    categories = models.ManyToManyField(
        EventCategory,
        related_name="events",
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if bool(self.created_by_user) == bool(self.created_by_org):
            raise ValidationError("Event must have exactly one creator: either a user or an organization.")
        # if self.pk and self.images.count() == 0:
        #     raise ValidationError("Event must have at least one image.")

    def __str__(self):
        return self.title

# -------------------------------
# Zdjęcia
# -------------------------------
class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="events/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.event.title}"

# -------------------------------
# Uczestnictwo
# -------------------------------
class EventParticipant(models.Model):
    STATUS_CHOICES = [
        ("registered", "Registered"),
        ("cancelled", "Cancelled"),
        ("waitlist", "Waitlist"),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="registered")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.user.username} → {self.event.title} ({self.status})"


@receiver(post_save, sender=EventParticipant)
def increase_participants(sender, instance, created, **kwargs):
    if created and instance.status == "registered":
        event = instance.event
        event.participants_count += 1
        event.save()
        
@receiver(post_delete, sender=EventParticipant)
def decrease_participants(sender, instance, **kwargs):
    if instance.status == "registered":
        event = instance.event
        event.participants_count -= 1
        event.save()