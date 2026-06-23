"""
Dashboard Views for Laver Transformation Ministries Church CMS
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import (
    Leadership, Ministry, ServiceTime, Event, Sermon,
    GalleryImage, Testimonial, Announcement, PrayerRequest,
    NewsletterSubscriber, GivingInfo, ContactMessage, ChurchInfo
)


def login_view(request):
    """Staff login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'dashboard/login.html')


def logout_view(request):
    """Staff logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('dashboard_login')


@login_required
def dashboard(request):
    """Main dashboard view with statistics"""
    context = {
        'total_leadership': Leadership.objects.count(),
        'total_ministries': Ministry.objects.count(),
        'total_events': Event.objects.count(),
        'total_sermons': Sermon.objects.count(),
        'total_gallery': GalleryImage.objects.count(),
        'pending_prayers': PrayerRequest.objects.filter(status='pending').count(),
        'pending_testimonials': Testimonial.objects.filter(is_approved=False).count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'newsletter_subscribers': NewsletterSubscriber.objects.filter(is_active=True).count(),
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
        'recent_prayers': PrayerRequest.objects.order_by('-date_submitted')[:5],
    }
    return render(request, 'dashboard/index.html', context)


# ===== Church Info =====
@login_required
def church_info(request):
    """Edit church information"""
    info = ChurchInfo.objects.first()
    if request.method == 'POST':
        info.name = request.POST.get('name')
        info.mission = request.POST.get('mission')
        info.vision = request.POST.get('vision')
        info.history = request.POST.get('history')
        info.address = request.POST.get('address')
        info.phone = request.POST.get('phone')
        info.phone_2 = request.POST.get('phone_2')
        info.email = request.POST.get('email')
        info.facebook = request.POST.get('facebook')
        info.instagram = request.POST.get('instagram')
        info.youtube = request.POST.get('youtube')
        info.whatsapp = request.POST.get('whatsapp')
        info.google_maps_embed = request.POST.get('google_maps_embed')
        info.welcome_message = request.POST.get('welcome_message')
        info.senior_pastor_name = request.POST.get('senior_pastor_name')
        info.senior_pastor_title = request.POST.get('senior_pastor_title')
        
        if request.FILES.get('logo'):
            info.logo = request.FILES.get('logo')
        
        info.save()
        messages.success(request, 'Church information updated successfully!')
        return redirect('church_info')
    
    return render(request, 'dashboard/church_info.html', {'info': info})


# ===== Leadership =====
@login_required
def leadership_list(request):
    """List all leadership members"""
    leaders = Leadership.objects.all().order_by('display_order')
    paginator = Paginator(leaders, 20)
    page = request.GET.get('page')
    leaders = paginator.get_page(page)
    return render(request, 'dashboard/leadership/list.html', {'leaders': leaders})

@login_required
def leadership_create(request):
    """Add new leadership member"""
    if request.method == 'POST':
        Leadership.objects.create(
            name=request.POST.get('name'),
            position=request.POST.get('position'),
            bio=request.POST.get('bio'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            display_order=request.POST.get('display_order', 0),
            is_active=True,
            photo=request.FILES.get('photo')
        )
        messages.success(request, 'Leadership member added successfully!')
        return redirect('leadership_list')
    return render(request, 'dashboard/leadership/form.html', {'action': 'Add'})

@login_required
def leadership_edit(request, pk):
    """Edit leadership member"""
    leader = get_object_or_404(Leadership, pk=pk)
    if request.method == 'POST':
        leader.name = request.POST.get('name')
        leader.position = request.POST.get('position')
        leader.bio = request.POST.get('bio')
        leader.email = request.POST.get('email')
        leader.phone = request.POST.get('phone')
        leader.display_order = request.POST.get('display_order', 0)
        leader.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('photo'):
            leader.photo = request.FILES.get('photo')
        leader.save()
        messages.success(request, 'Leadership member updated successfully!')
        return redirect('leadership_list')
    return render(request, 'dashboard/leadership/form.html', {'leader': leader, 'action': 'Edit'})

@login_required
def leadership_delete(request, pk):
    """Delete leadership member"""
    leader = get_object_or_404(Leadership, pk=pk)
    leader.delete()
    messages.success(request, 'Leadership member deleted successfully!')
    return redirect('leadership_list')


# ===== Ministries =====
@login_required
def ministries_list(request):
    """List all ministries"""
    ministries = Ministry.objects.all().order_by('display_order')
    return render(request, 'dashboard/ministries/list.html', {'ministries': ministries})

@login_required
def ministry_create(request):
    """Add new ministry"""
    leaders = Leadership.objects.filter(is_active=True)
    if request.method == 'POST':
        Ministry.objects.create(
            name=request.POST.get('name'),
            slug=request.POST.get('slug') or None,
            description=request.POST.get('description'),
            icon=request.POST.get('icon'),
            leader_id=request.POST.get('leader'),
            display_order=request.POST.get('display_order', 0),
            is_active=True,
            image=request.FILES.get('image')
        )
        messages.success(request, 'Ministry added successfully!')
        return redirect('ministries_list')
    return render(request, 'dashboard/ministries/form.html', {'leaders': leaders, 'action': 'Add'})

@login_required
def ministry_edit(request, pk):
    """Edit ministry"""
    ministry = get_object_or_404(Ministry, pk=pk)
    leaders = Leadership.objects.filter(is_active=True)
    if request.method == 'POST':
        ministry.name = request.POST.get('name')
        ministry.slug = request.POST.get('slug')
        ministry.description = request.POST.get('description')
        ministry.icon = request.POST.get('icon')
        ministry.leader_id = request.POST.get('leader')
        ministry.display_order = request.POST.get('display_order', 0)
        ministry.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            ministry.image = request.FILES.get('image')
        ministry.save()
        messages.success(request, 'Ministry updated successfully!')
        return redirect('ministries_list')
    return render(request, 'dashboard/ministries/form.html', {'ministry': ministry, 'leaders': leaders, 'action': 'Edit'})

@login_required
def ministry_delete(request, pk):
    """Delete ministry"""
    ministry = get_object_or_404(Ministry, pk=pk)
    ministry.delete()
    messages.success(request, 'Ministry deleted successfully!')
    return redirect('ministries_list')


# ===== Service Times =====
@login_required
def service_times_list(request):
    """List all service times"""
    services = ServiceTime.objects.all().order_by('display_order')
    return render(request, 'dashboard/service_times/list.html', {'services': services})

@login_required
def service_time_create(request):
    """Add new service time"""
    if request.method == 'POST':
        ServiceTime.objects.create(
            name=request.POST.get('name'),
            day=request.POST.get('day'),
            time=request.POST.get('time'),
            description=request.POST.get('description'),
            display_order=request.POST.get('display_order', 0),
            is_active=True
        )
        messages.success(request, 'Service time added successfully!')
        return redirect('service_times_list')
    return render(request, 'dashboard/service_times/form.html', {'action': 'Add'})

@login_required
def service_time_edit(request, pk):
    """Edit service time"""
    service = get_object_or_404(ServiceTime, pk=pk)
    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.day = request.POST.get('day')
        service.time = request.POST.get('time')
        service.description = request.POST.get('description')
        service.display_order = request.POST.get('display_order', 0)
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()
        messages.success(request, 'Service time updated successfully!')
        return redirect('service_times_list')
    return render(request, 'dashboard/service_times/form.html', {'service': service, 'action': 'Edit'})

@login_required
def service_time_delete(request, pk):
    """Delete service time"""
    service = get_object_or_404(ServiceTime, pk=pk)
    service.delete()
    messages.success(request, 'Service time deleted successfully!')
    return redirect('service_times_list')


# ===== Events =====
@login_required
def events_list(request):
    """List all events"""
    events = Event.objects.all().order_by('-start_date')
    paginator = Paginator(events, 20)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    return render(request, 'dashboard/events/list.html', {'events': events})

@login_required
def event_create(request):
    """Add new event"""
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            slug=request.POST.get('slug') or None,
            description=request.POST.get('description'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date') or None,
            location=request.POST.get('location'),
            registration_link=request.POST.get('registration_link'),
            is_featured=request.POST.get('is_featured') == 'on',
            is_published=request.POST.get('is_published') == 'on',
            image=request.FILES.get('image')
        )
        messages.success(request, 'Event added successfully!')
        return redirect('dashboard_events')
    return render(request, 'dashboard/events/form.html', {'action': 'Add'})

@login_required
def event_edit(request, pk):
    """Edit event"""
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.slug = request.POST.get('slug')
        event.description = request.POST.get('description')
        event.start_date = request.POST.get('start_date')
        event.end_date = request.POST.get('end_date') or None
        event.location = request.POST.get('location')
        event.registration_link = request.POST.get('registration_link')
        event.is_featured = request.POST.get('is_featured') == 'on'
        event.is_published = request.POST.get('is_published') == 'on'
        if request.FILES.get('image'):
            event.image = request.FILES.get('image')
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('dashboard_events')
    return render(request, 'dashboard/events/form.html', {'event': event, 'action': 'Edit'})

@login_required
def event_delete(request, pk):
    """Delete event"""
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('dashboard_events')


# ===== Sermons =====
@login_required
def sermons_list(request):
    """List all sermons"""
    sermons = Sermon.objects.all().order_by('-date_preached')
    paginator = Paginator(sermons, 20)
    page = request.GET.get('page')
    sermons = paginator.get_page(page)
    return render(request, 'dashboard/sermons/list.html', {'sermons': sermons})

@login_required
def sermon_create(request):
    """Add new sermon"""
    speakers = Leadership.objects.filter(is_active=True)
    if request.method == 'POST':
        Sermon.objects.create(
            title=request.POST.get('title'),
            slug=request.POST.get('slug') or None,
            speaker_id=request.POST.get('speaker'),
            date_preached=request.POST.get('date_preached'),
            description=request.POST.get('description'),
            video_url=request.POST.get('video_url'),
            audio_url=request.FILES.get('audio_url'),
            sermon_notes=request.FILES.get('sermon_notes'),
            is_featured=request.POST.get('is_featured') == 'on',
            is_published=request.POST.get('is_published') == 'on'
        )
        messages.success(request, 'Sermon added successfully!')
        return redirect('dashboard_sermons')
    return render(request, 'dashboard/sermons/form.html', {'speakers': speakers, 'action': 'Add'})

@login_required
def sermon_edit(request, pk):
    """Edit sermon"""
    sermon = get_object_or_404(Sermon, pk=pk)
    speakers = Leadership.objects.filter(is_active=True)
    if request.method == 'POST':
        sermon.title = request.POST.get('title')
        sermon.slug = request.POST.get('slug')
        sermon.speaker_id = request.POST.get('speaker')
        sermon.date_preached = request.POST.get('date_preached')
        sermon.description = request.POST.get('description')
        sermon.video_url = request.POST.get('video_url')
        sermon.is_featured = request.POST.get('is_featured') == 'on'
        sermon.is_published = request.POST.get('is_published') == 'on'
        if request.FILES.get('audio_url'):
            sermon.audio_url = request.FILES.get('audio_url')
        if request.FILES.get('sermon_notes'):
            sermon.sermon_notes = request.FILES.get('sermon_notes')
        sermon.save()
        messages.success(request, 'Sermon updated successfully!')
        return redirect('dashboard_sermons')
    return render(request, 'dashboard/sermons/form.html', {'sermon': sermon, 'speakers': speakers, 'action': 'Edit'})

@login_required
def sermon_delete(request, pk):
    """Delete sermon"""
    sermon = get_object_or_404(Sermon, pk=pk)
    sermon.delete()
    messages.success(request, 'Sermon deleted successfully!')
    return redirect('dashboard_sermons')


# ===== Gallery =====
@login_required
def gallery_list(request):
    """List all gallery images"""
    images = GalleryImage.objects.all().order_by('-date_uploaded')
    paginator = Paginator(images, 24)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    return render(request, 'dashboard/gallery/list.html', {'images': images})

@login_required
def gallery_image_create(request):
    """Add new gallery image"""
    albums = GalleryAlbum.objects.all()
    if request.method == 'POST':
        GalleryImage.objects.create(
            album_id=request.POST.get('album'),
            image=request.FILES.get('image'),
            caption=request.POST.get('caption'),
            is_active=True
        )
        messages.success(request, 'Image added to gallery successfully!')
        return redirect('dashboard_gallery')
    return render(request, 'dashboard/gallery/form.html', {'albums': albums})

@login_required
def gallery_image_delete(request, pk):
    """Delete gallery image"""
    image = get_object_or_404(GalleryImage, pk=pk)
    image.delete()
    messages.success(request, 'Image deleted successfully!')
    return redirect('dashboard_gallery')


# ===== Testimonials =====
@login_required
def testimonials_list(request):
    """List all testimonials"""
    testimonials = Testimonial.objects.all().order_by('-date_submitted')
    paginator = Paginator(testimonials, 20)
    page = request.GET.get('page')
    testimonials = paginator.get_page(page)
    return render(request, 'dashboard/testimonials/list.html', {'testimonials': testimonials})

@login_required
def testimonial_create(request):
    """Add new testimonial"""
    if request.method == 'POST':
        Testimonial.objects.create(
            name=request.POST.get('name'),
            testimony=request.POST.get('testimony'),
            is_approved=request.POST.get('is_approved') == 'on',
            is_featured=request.POST.get('is_featured') == 'on',
            photo=request.FILES.get('photo')
        )
        messages.success(request, 'Testimonial added successfully!')
        return redirect('testimonials_list')
    return render(request, 'dashboard/testimonials/form.html', {'action': 'Add'})

@login_required
def testimonial_edit(request, pk):
    """Edit testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        testimonial.name = request.POST.get('name')
        testimonial.testimony = request.POST.get('testimony')
        testimonial.is_approved = request.POST.get('is_approved') == 'on'
        testimonial.is_featured = request.POST.get('is_featured') == 'on'
        if request.FILES.get('photo'):
            testimonial.photo = request.FILES.get('photo')
        testimonial.save()
        messages.success(request, 'Testimonial updated successfully!')
        return redirect('testimonials_list')
    return render(request, 'dashboard/testimonials/form.html', {'testimonial': testimonial, 'action': 'Edit'})

@login_required
def testimonial_delete(request, pk):
    """Delete testimonial"""
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('testimonials_list')


# ===== Announcements =====
@login_required
def announcements_list(request):
    """List all announcements"""
    announcements = Announcement.objects.all().order_by('-publish_date')
    return render(request, 'dashboard/announcements/list.html', {'announcements': announcements})

@login_required
def announcement_create(request):
    """Add new announcement"""
    if request.method == 'POST':
        Announcement.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            publish_date=request.POST.get('publish_date'),
            expiry_date=request.POST.get('expiry_date') or None,
            is_active=True
        )
        messages.success(request, 'Announcement added successfully!')
        return redirect('announcements_list')
    return render(request, 'dashboard/announcements/form.html', {'action': 'Add'})

@login_required
def announcement_edit(request, pk):
    """Edit announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.content = request.POST.get('content')
        announcement.publish_date = request.POST.get('publish_date')
        announcement.expiry_date = request.POST.get('expiry_date') or None
        announcement.is_active = request.POST.get('is_active') == 'on'
        announcement.save()
        messages.success(request, 'Announcement updated successfully!')
        return redirect('announcements_list')
    return render(request, 'dashboard/announcements/form.html', {'announcement': announcement, 'action': 'Edit'})

@login_required
def announcement_delete(request, pk):
    """Delete announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, 'Announcement deleted successfully!')
    return redirect('announcements_list')


# ===== Prayer Requests =====
@login_required
def prayer_requests_list(request):
    """List all prayer requests"""
    prayers = PrayerRequest.objects.all().order_by('-date_submitted')
    paginator = Paginator(prayers, 25)
    page = request.GET.get('page')
    prayers = paginator.get_page(page)
    return render(request, 'dashboard/prayer_requests/list.html', {'prayers': prayers})

@login_required
def prayer_request_update(request, pk):
    """Update prayer request status"""
    prayer = get_object_or_404(PrayerRequest, pk=pk)
    if request.method == 'POST':
        prayer.status = request.POST.get('status')
        prayer.save()
        messages.success(request, 'Prayer request updated successfully!')
    return redirect('prayer_requests_list')


# ===== Newsletter =====
@login_required
def newsletter_list(request):
    """List all newsletter subscribers"""
    subscribers = NewsletterSubscriber.objects.all().order_by('-date_subscribed')
    paginator = Paginator(subscribers, 30)
    page = request.GET.get('page')
    subscribers = paginator.get_page(page)
    return render(request, 'dashboard/newsletter/list.html', {'subscribers': subscribers})


# ===== Messages =====
@login_required
def messages_list(request):
    """List all contact messages"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    paginator = Paginator(messages_list, 25)
    page = request.GET.get('page')
    messages_qs = paginator.get_page(page)
    return render(request, 'dashboard/messages/list.html', {'messages': messages_qs})

@login_required
def message_detail(request, pk):
    """View message detail"""
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'dashboard/messages/detail.html', {'message': message})


# ===== Giving Info =====
@login_required
def giving_info(request):
    """Edit giving information"""
    info = GivingInfo.objects.first()
    if not info:
        info = GivingInfo.objects.create(title='Support Our Ministry')
    
    if request.method == 'POST':
        info.title = request.POST.get('title')
        info.description = request.POST.get('description')
        info.mtn_mobile = request.POST.get('mtn_mobile')
        info.airtel_mobile = request.POST.get('airtel_mobile')
        info.bank_name = request.POST.get('bank_name')
        info.bank_account_name = request.POST.get('bank_account_name')
        info.bank_account_number = request.POST.get('bank_account_number')
        info.bank_swift_code = request.POST.get('bank_swift_code')
        info.paypal_email = request.POST.get('paypal_email')
        info.flutterwave_details = request.POST.get('flutterwave_details')
        info.save()
        messages.success(request, 'Giving information updated successfully!')
        return redirect('giving_info')
    
    return render(request, 'dashboard/giving_info.html', {'info': info})


# Add GalleryAlbum model import at top if missing
from .models import GalleryAlbum
