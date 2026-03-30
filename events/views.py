from django.http import JsonResponse
from .models import Event
from django.shortcuts import render

def index(request):
    return render(request, "events/event_list.html")

def event_list(request):
    events = Event.objects.all().order_by("start_datetime")

    data = [
        {
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "start_datetime": event.start_datetime.isoformat(),
        }
        for event in events
    ]

    return JsonResponse(data, safe=False)