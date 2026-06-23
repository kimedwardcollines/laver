"""
Context Processors for Church CMS
"""
from .models import ChurchInfo, GivingInfo, Announcement


def church_info(request):
    """Add church info to all templates"""
    church = ChurchInfo.objects.first()
    giving = GivingInfo.objects.filter(is_active=True).first()
    announcements = Announcement.objects.filter(is_active=True)
    
    return {
        'church': church,
        'giving_info': giving,
        'announcements': announcements,
    }
