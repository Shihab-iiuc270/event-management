from datetime import date

from django.shortcuts import render

from events.models import Category, Event


def home(request):
    category_name = request.GET.get("cat")

    base_qs = Event.objects.select_related("category").all()
    today = date.today()
    upcoming_qs = base_qs.filter(date__gte=today).order_by("date", "time")

    # Home page should show *all* events (upcoming + past).
    events_qs = base_qs
    if category_name:
        events_qs = events_qs.filter(category__name=category_name)

    upcoming_events = list(events_qs.filter(date__gte=today).order_by("date", "time"))
    past_events = list(events_qs.filter(date__lt=today).order_by("-date", "-time"))

    context = {
        "categories": Category.objects.all().order_by("name"),
        "latest_events": list(upcoming_qs[:4]),
        "featured_events": list(upcoming_qs[:2]),
        "events": upcoming_events + past_events,
        "active_category": category_name or "All",
    }
    return render(request, "home.html", context)

def no_permission(request):
    return render(request,'no_permission.html')
