from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField


class ChurchInfo(models.Model):
    """Single church information record"""
    name = models.CharField(max_length=200, default='Laver Transformation Ministries')
    senior_pastor_name = models.CharField(max_length=200)
    senior_pastor_title = models.CharField(max_length=100, default='Senior Pastor')
    address = models.TextField()
    phone = models.CharField(max_length=50)
    phone_2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    welcome_message = RichTextField(blank=True)
    mission = RichTextField(blank=True)
    vision = RichTextField(blank=True)
    history = RichTextField(blank=True)
    logo = models.ImageField(upload_to='church/', blank=True)
    
    class Meta:
        verbose_name = 'Church Information'
        verbose_name_plural = 'Church Information'
    
    def __str__(self):
        return self.name


class Leadership(models.Model):
    """Church leadership team"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    bio = RichTextField(blank=True)
    photo = models.ImageField(upload_to='leadership/', blank=True)
    is_active = models.BooleanField(default=True)
    is_senior_pastor = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Leadership'
    
    def __str__(self):
        return f"{self.name} - {self.position}"


class Ministry(models.Model):
    """Church ministry"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()
    icon = models.CharField(max_length=100, default='fa-church')
    image = models.ImageField(upload_to='ministries/', blank=True)
    leader = models.ForeignKey(Leadership, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_ministries')
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Ministries'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('ministry_detail', kwargs={'slug': self.slug})


class ServiceTime(models.Model):
    """Weekly service times"""
    name = models.CharField(max_length=100)
    day = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'day', 'time']
    
    def __str__(self):
        return f"{self.name}: {self.day} at {self.time}"


class Event(models.Model):
    """Church events"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='events/', blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})


class Sermon(models.Model):
    """Sermons"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    speaker = models.CharField(max_length=200)
    date_preached = models.DateField()
    description = RichTextField()
    video_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    sermon_notes = RichTextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_preached']
        verbose_name_plural = 'Sermons'
    
    def __str__(self):
        return f"{self.title} - {self.speaker}"
    
    def get_absolute_url(self):
        return reverse('sermon_detail', kwargs={'slug': self.slug})


class GalleryImage(models.Model):
    """Gallery images"""
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Gallery Images'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title or f"Image {self.id}"


class Testimonial(models.Model):
    """Testimonials from members"""
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='testimonials/', blank=True)
    testimony = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_submitted']
    
    def __str__(self):
        return f"{self.name} - {self.testimony[:50]}..."


class PrayerRequest(models.Model):
    """Prayer requests from visitors"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    request_text = models.TextField()
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prayer Request from {self.name}"


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name}: {self.subject or self.message[:50]}"


class GivingInfo(models.Model):
    """Giving information and bank details"""
    title = models.CharField(max_length=200, default='Support Our Ministry')
    description = RichTextField(blank=True)
    mtn_mobile = models.CharField(max_length=100, blank=True)
    airtel_mobile = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'Giving Information'
        verbose_name_plural = 'Giving Information'
    
    def __str__(self):
        return self.title


class Announcement(models.Model):
    """Announcements"""
    title = models.CharField(max_length=200)
    content = RichTextField()
    is_published = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
    
    def __str__(self):
        return self.title
