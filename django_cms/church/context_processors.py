from .models import ChurchInfo, ServiceTime, Announcement


def church_info(request):
    """Add church info to all templates"""
    church = ChurchInfo.objects.first()
    service_times = ServiceTime.objects.filter(is_active=True)
    announcements = Announcement.objects.filter(is_published=True)
    
    return {
        'church': church,
        'service_times': service_times,
        'announcements': announcements,
    }
