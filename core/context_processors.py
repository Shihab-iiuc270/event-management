def ui_permissions(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"can_rsvp": False}

    privileged = user.is_superuser or user.groups.filter(name__in=["admin", "organiser"]).exists()
    return {"can_rsvp": not privileged}

