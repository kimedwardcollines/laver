"""
Django Admin Configuration for Laver Transformation Ministries Church CMS
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
    ChurchInfo, Leadership, Ministry, ServiceTime, Event, Sermon,
    GalleryAlbum, GalleryImage, Testimonial, Announcement,
    PrayerRequest, NewsletterSubscriber, GivingInfo, ContactMessage
)


# Inline for Gallery Images
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'caption', 'is_active']
    readonly_fields = ['date_uploaded']


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    inlines = [GalleryImageInline]
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'caption', 'album', 'date_uploaded', 'is_active']
    list_filter = ['is_active', 'album', 'date_uploaded']
    search_fields = ['caption', 'album__name']
    readonly_fields = ['date_uploaded']
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px;">')
        return '-'
    thumbnail.short_description = 'Image'


# Church Info Admin
@admin.register(ChurchInfo)
class ChurchInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'senior_pastor_name', 'senior_pastor_title', 'welcome_message')
        }),
        ('Mission & Vision', {
            'fields': ('mission', 'vision', 'history')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'phone_2', 'email')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'youtube', 'whatsapp')
        }),
        ('Maps', {
            'fields': ('google_maps_embed',)
        }),
    )
    
    def has_add_permission(self, request):
        return not ChurchInfo.objects.exists()


# Leadership Admin
@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'name', 'position', 'email', 'is_active', 'display_order']
    list_filter = ['is_active', 'position']
    search_fields = ['name', 'position', 'email']
    list_editable = ['display_order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">')
        return format_html('<i class="fas fa-user" style="font-size: 24px; color: #ccc;"></i>')
    photo_thumbnail.short_description = 'Photo'


# Ministry Admin
@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'icon', 'is_active', 'display_order']
    list_filter = ['is_active', 'leader']
    search_fields = ['name', 'description']
    list_editable = ['display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


# Service Time Admin
@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'time', 'is_active', 'display_order']
    list_filter = ['day', 'is_active']
    list_editable = ['is_active', 'display_order']
    ordering = ['display_order', 'day', 'time']


# Event Admin
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['image_thumbnail', 'title', 'start_date', 'location', 'is_featured', 'is_published']
    list_filter = ['is_published', 'is_featured', 'start_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'location', 'registration_link')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 5px;">')
        return '-'
    image_thumbnail.short_description = 'Image'


# Sermon Admin
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'date_preached', 'is_featured', 'is_published']
    list_filter = ['is_published', 'is_featured', 'date_preached', 'speaker']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_published']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at']
    date_hierarchy = 'date_preached'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'speaker', 'date_preached', 'description')
        }),
        ('Media', {
            'fields': ('video_url', 'audio_url', 'sermon_notes')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
    )


# Testimonial Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['photo_thumbnail', 'name', 'testimony_preview', 'is_approved', 'is_featured', 'date_submitted']
    list_filter = ['is_approved', 'is_featured', 'date_submitted']
    search_fields = ['name', 'testimony']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['date_submitted']
    
    def testimony_preview(self, obj):
        return obj.testimony[:100] + '...' if len(obj.testimony) > 100 else obj.testimony
    testimony_preview.short_description = 'Testimony'
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;">')
        return format_html('<i class="fas fa-user" style="font-size: 24px; color: #ccc;"></i>')
    photo_thumbnail.short_description = 'Photo'
    
    actions = ['approve_testimonials', 'reject_testimonials']
    
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)
    approve_testimonials.short_description = 'Approve selected testimonials'
    
    def reject_testimonials(self, request, queryset):
        queryset.update(is_approved=False)
    reject_testimonials.short_description = 'Reject selected testimonials'


# Announcement Admin
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'publish_date', 'expiry_date', 'is_active', 'is_valid_display']
    list_filter = ['is_active', 'publish_date']
    search_fields = ['title', 'content']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    date_hierarchy = 'publish_date'
    
    def is_valid_display(self, obj):
        return obj.is_valid()
    is_valid_display.boolean = True
    is_valid_display.short_description = 'Valid'


# Prayer Request Admin
@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'request_preview', 'date_submitted', 'status']
    list_filter = ['status', 'date_submitted']
    search_fields = ['name', 'email', 'request']
    list_editable = ['status']
    readonly_fields = ['date_submitted']
    actions = ['mark_reviewed', 'mark_answered']
    
    def request_preview(self, obj):
        return obj.request[:50] + '...' if len(obj.request) > 50 else obj.request
    request_preview.short_description = 'Request'
    
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_reviewed.short_description = 'Mark as reviewed'
    
    def mark_answered(self, request, queryset):
        queryset.update(status='answered')
    mark_answered.short_description = 'Mark as answered'


# Newsletter Subscriber Admin
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'date_subscribed', 'is_active']
    list_filter = ['is_active', 'date_subscribed']
    search_fields = ['email']
    list_editable = ['is_active']
    readonly_fields = ['date_subscribed']
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = 'Activate selected'
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = 'Deactivate selected'


# Giving Info Admin
@admin.register(GivingInfo)
class GivingInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'mtn_mobile', 'airtel_mobile', 'is_active']
    list_editable = ['is_active']
    
    def has_add_permission(self, request):
        return not GivingInfo.objects.exists()


# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'subject', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark as unread'


# Customize Admin Site
admin.site.site_header = 'Laver Transformation Ministries CMS'
admin.site.site_title = 'Laver CMS Admin'
admin.site.index_title = 'Dashboard'
