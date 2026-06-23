"""
Django Models for Laver Transformation Ministries Church CMS
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from datetime import datetime


class ChurchInfo(models.Model):
    """Church general information - singleton model"""
    name = models.CharField(max_length=200, default='Laver Transformation Ministries')
    logo = models.ImageField(upload_to='church/', blank=True, null=True)
    mission = RichTextField(blank=True, default='')
    vision = RichTextField(blank=True, default='')
    history = RichTextField(blank=True, default='')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    phone_2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    google_maps_embed = models.TextField(blank=True, help_text='Embed URL for Google Maps')
    welcome_message = RichTextField(blank=True)
    senior_pastor_name = models.CharField(max_length=100, blank=True)
    senior_pastor_title = models.CharField(max_length=100, blank=True, default='Senior Pastor')
    
    class Meta:
        verbose_name = 'Church Information'
        verbose_name_plural = 'Church Information'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and ChurchInfo.objects.exists():
            return self.pk
        return super().save(*args, **kwargs)


class Leadership(models.Model):
    """Church leadership team members"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True)
    bio = RichTextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Leader'
        verbose_name_plural = 'Leadership'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Ministry(models.Model):
    """Church ministries"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = RichTextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon class')
    image = models.ImageField(upload_to='ministries/', blank=True, null=True)
    leader = models.ForeignKey(Leadership, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_ministries')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Ministry'
        verbose_name_plural = 'Ministries'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ServiceTime(models.Model):
    """Weekly service schedules"""
    name = models.CharField(max_length=100)
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'day', 'time']
        verbose_name = 'Service Time'
        verbose_name_plural = 'Service Times'
    
    def __str__(self):
        return f"{self.name} - {self.day} at {self.time}"


class Event(models.Model):
    """Church events"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    registration_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Sermon(models.Model):
    """Sermons"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    speaker = models.ForeignKey(Leadership, on_delete=models.SET_NULL, null=True, blank=True)
    date_preached = models.DateField()
    description = RichTextField(blank=True)
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    audio_url = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    sermon_notes = models.FileField(upload_to='sermons/notes/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_preached']
        verbose_name = 'Sermon'
        verbose_name_plural = 'Sermons'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class GalleryAlbum(models.Model):
    """Photo gallery albums"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/albums/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Gallery Album'
        verbose_name_plural = 'Gallery Albums'
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Gallery images"""
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_uploaded']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.caption or f"Image {self.id}"


class Testimonial(models.Model):
    """Member testimonials"""
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    testimony = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_submitted']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
    
    def __str__(self):
        return f"{self.name} - {self.date_submitted.strftime('%Y-%m-%d')}"


class Announcement(models.Model):
    """Church announcements"""
    title = models.CharField(max_length=200)
    content = RichTextField()
    publish_date = models.DateTimeField()
    expiry_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-publish_date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
    
    def is_valid(self):
        from django.utils import timezone
        if not self.is_active:
            return False
        if self.expiry_date and self.expiry_date < timezone.now():
            return False
        return True
    
    def __str__(self):
        return self.title


class PrayerRequest(models.Model):
    """Prayer requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('answered', 'Answered'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    request = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-date_submitted']
        verbose_name = 'Prayer Request'
        verbose_name_plural = 'Prayer Requests'
    
    def __str__(self):
        return f"{self.name} - {self.date_submitted.strftime('%Y-%m-%d')}"


class NewsletterSubscriber(models.Model):
    """Newsletter subscribers"""
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_subscribed']
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'
    
    def __str__(self):
        return self.email


class GivingInfo(models.Model):
    """Online giving information"""
    title = models.CharField(max_length=100, default='Support Our Ministry')
    description = RichTextField(blank=True)
    # Mobile Money
    mtn_mobile = models.CharField(max_length=50, blank=True, verbose_name='MTN Mobile Money')
    airtel_mobile = models.CharField(max_length=50, blank=True, verbose_name='Airtel Money')
    # Bank
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_swift_code = models.CharField(max_length=20, blank=True)
    # PayPal
    paypal_email = models.EmailField(blank=True)
    # Flutterwave
    flutterwave_details = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Giving Information'
        verbose_name_plural = 'Giving Information'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk and GivingInfo.objects.exists():
            return self.pk
        return super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Contact form messages"""
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('prayer', 'Prayer Request'),
        ('visit', 'Planning a Visit'),
        ('volunteer', 'Volunteer Opportunities'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
