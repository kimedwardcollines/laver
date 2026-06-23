"""
Views for Laver Transformation Ministries Church Website
"""
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (
    ChurchInfo, Leadership, Ministry, ServiceTime, Event, Sermon,
    GalleryImage, Testimonial, Announcement, PrayerRequest,
    NewsletterSubscriber, GivingInfo, ContactMessage
)


class HomeView(TemplateView):
    """Homepage view - dynamically loads all content"""
    template_name = 'church/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Church Info
        context['church'] = ChurchInfo.objects.first()
        
        # Service Times
        context['service_times'] = ServiceTime.objects.filter(is_active=True)[:4]
        
        # Active Ministries
        context['ministries'] = Ministry.objects.filter(is_active=True)[:6]
        
        # Featured Events (upcoming)
        context['events'] = Event.objects.filter(
            is_published=True
        ).order_by('start_date')[:4]
        
        # Latest Sermons
        context['sermons'] = Sermon.objects.filter(
            is_published=True
        ).order_by('-date_preached')[:3]
        
        # Active Testimonials (approved and featured)
        context['testimonials'] = Testimonial.objects.filter(
            is_approved=True, is_featured=True
        )[:3]
        
        # Gallery Images
        context['gallery_images'] = GalleryImage.objects.filter(
            is_active=True
        ).order_by('-date_uploaded')[:6]
        
        # Active Announcements
        context['announcements'] = Announcement.objects.filter(is_active=True)
        
        # Giving Info
        context['giving_info'] = GivingInfo.objects.filter(is_active=True).first()
        
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'church/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = ChurchInfo.objects.first()
        context['leadership'] = Leadership.objects.filter(is_active=True)
        context['ministries'] = Ministry.objects.filter(is_active=True)
        return context


class MinistriesView(ListView):
    """Ministries listing view"""
    model = Ministry
    template_name = 'church/ministries.html'
    context_object_name = 'ministries'
    paginate_by = 9
    
    def get_queryset(self):
        return Ministry.objects.filter(is_active=True).order_by('display_order')


class MinistryDetailView(DetailView):
    """Ministry detail view"""
    model = Ministry
    template_name = 'church/ministry_detail.html'
    context_object_name = 'ministry'
    queryset = Ministry.objects.filter(is_active=True)


class EventsView(ListView):
    """Events listing view"""
    model = Event
    template_name = 'church/events.html'
    context_object_name = 'events'
    paginate_by = 9
    
    def get_queryset(self):
        return Event.objects.filter(is_published=True).order_by('-start_date')


class EventDetailView(DetailView):
    """Event detail view"""
    model = Event
    template_name = 'church/event_detail.html'
    context_object_name = 'event'
    queryset = Event.objects.filter(is_published=True)


class SermonsView(ListView):
    """Sermons listing view"""
    model = Sermon
    template_name = 'church/sermons.html'
    context_object_name = 'sermons'
    paginate_by = 12
    
    def get_queryset(self):
        return Sermon.objects.filter(is_published=True).order_by('-date_preached')


class SermonDetailView(DetailView):
    """Sermon detail view"""
    model = Sermon
    template_name = 'church/sermon_detail.html'
    context_object_name = 'sermon'
    queryset = Sermon.objects.filter(is_published=True)


class GalleryView(ListView):
    """Gallery view"""
    model = GalleryImage
    template_name = 'church/gallery.html'
    context_object_name = 'images'
    paginate_by = 24
    
    def get_queryset(self):
        return GalleryImage.objects.filter(is_active=True).order_by('-date_uploaded')


class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'church/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['church'] = ChurchInfo.objects.first()
        return context


def contact_form_submit(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', 'general')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return HttpResponseRedirect(reverse('contact'))
    
    return HttpResponseRedirect(reverse('contact'))


class PrayerRequestView(TemplateView):
    """Prayer request page view"""
    template_name = 'church/prayer_request.html'


def prayer_request_submit(request):
    """Handle prayer request submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        prayer_request = request.POST.get('request')
        
        PrayerRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            request=prayer_request
        )
        
        messages.success(request, 'Your prayer request has been submitted. Our prayer team will pray for you.')
        return HttpResponseRedirect(reverse('prayer_request'))
    
    return HttpResponseRedirect(reverse('prayer_request'))


class GiveView(TemplateView):
    """Give/Donate page view"""
    template_name = 'church/give.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['giving_info'] = GivingInfo.objects.filter(is_active=True).first()
        return context


def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
            
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    return HttpResponseRedirect('/')


# Sitemap
from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'ministries', 'events', 'sermons', 'gallery', 'contact', 'prayer_request', 'give']
    
    def location(self, item):
        return reverse(item)
