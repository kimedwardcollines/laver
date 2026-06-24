from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    ChurchInfo, Leadership, Ministry, ServiceTime,
    Event, Sermon, GalleryImage, Testimonial,
    PrayerRequest, ContactMessage, GivingInfo, Announcement
)


def home(request):
    featured_sermons = Sermon.objects.filter(is_published=True, is_featured=True)[:3]
    upcoming_events = Event.objects.filter(is_published=True).order_by('start_date')[:3]
    testimonials = Testimonial.objects.filter(is_approved=True, is_featured=True)[:3]
    announcements = Announcement.objects.filter(is_published=True)[:3]
    
    context = {
        'featured_sermons': featured_sermons,
        'upcoming_events': upcoming_events,
        'testimonials': testimonials,
        'announcements': announcements,
    }
    return render(request, 'church/home.html', context)


def about(request):
    leadership = Leadership.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    
    context = {
        'leadership': leadership,
        'testimonials': testimonials,
    }
    return render(request, 'church/about.html', context)


def ministries(request):
    ministries = Ministry.objects.filter(is_active=True)
    context = {'ministries': ministries}
    return render(request, 'church/ministries.html', context)


def ministry_detail(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)
    context = {'ministry': ministry}
    return render(request, 'church/ministry_detail.html', context)


def sermons(request):
    sermons_list = Sermon.objects.filter(is_published=True)
    paginator = Paginator(sermons_list, 6)
    page = request.GET.get('page')
    sermons = paginator.get_page(page)
    context = {'sermons': sermons}
    return render(request, 'church/sermons.html', context)


def sermon_detail(request, slug):
    sermon = get_object_or_404(Sermon, slug=slug)
    related = Sermon.objects.filter(is_published=True).exclude(id=sermon.id)[:3]
    context = {'sermon': sermon, 'related_sermons': related}
    return render(request, 'church/sermon_detail.html', context)


def events(request):
    events_list = Event.objects.filter(is_published=True)
    paginator = Paginator(events_list, 6)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    context = {'events': events}
    return render(request, 'church/events.html', context)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related = Event.objects.filter(is_published=True).exclude(id=event.id)[:3]
    context = {'event': event, 'related_events': related}
    return render(request, 'church/event_detail.html', context)


def gallery(request):
    images = GalleryImage.objects.filter(is_published=True)
    context = {'images': images}
    return render(request, 'church/gallery.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name, email=email, phone=phone, subject=subject, message=message
        )
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'church/contact.html')


def give(request):
    giving_info = GivingInfo.objects.first()
    context = {'giving_info': giving_info}
    return render(request, 'church/give.html', context)


def prayer_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        request_text = request.POST.get('request')
        
        PrayerRequest.objects.create(
            name=name, email=email, phone=phone, request_text=request_text
        )
        messages.success(request, 'Your prayer request has been submitted. Our prayer team will pray for you.')
        return redirect('prayer_request')
    
    return render(request, 'church/prayer_request.html')
