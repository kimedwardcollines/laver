from django.contrib import admin
from .models import (
    ChurchInfo, Leadership, Ministry, ServiceTime,
    Event, Sermon, GalleryImage, Testimonial,
    PrayerRequest, ContactMessage, GivingInfo, Announcement
)


@admin.register(ChurchInfo)
class ChurchInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'senior_pastor_name', 'phone', 'email')
    fieldsets = (
        ('Church Details', {
            'fields': ('name', 'logo')
        }),
        ('Senior Pastor', {
            'fields': ('senior_pastor_name', 'senior_pastor_title')
        }),
        ('Contact Information', {
            'fields': ('address', 'phone', 'phone_2', 'email', 'facebook', 'instagram', 'youtube', 'whatsapp')
        }),
        ('About', {
            'fields': ('welcome_message', 'mission', 'vision', 'history')
        }),
    )


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_active', 'is_senior_pastor', 'display_order')
    list_filter = ('is_active', 'is_senior_pastor')
    search_fields = ('name', 'position')
    ordering = ('display_order', 'name')


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('display_order', 'name')


@admin.register(ServiceTime)
class ServiceTimeAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'time', 'is_active', 'display_order')
    list_filter = ('is_active',)
    ordering = ('display_order', 'day', 'time')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'location', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-start_date',)


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'date_preached', 'is_featured', 'is_published')
    list_filter = ('is_published', 'is_featured', 'speaker')
    search_fields = ('title', 'description', 'speaker')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-date_preached',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'caption')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_submitted', 'is_approved', 'is_featured')
    list_filter = ('is_approved', 'is_featured')
    search_fields = ('name', 'testimony')


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_answered')
    list_filter = ('is_answered',)
    search_fields = ('name', 'email', 'request_text')
    ordering = ('-created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)


@admin.register(GivingInfo)
class GivingInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'bank_name', 'account_number')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_pinned', 'valid_from', 'valid_until')
    list_filter = ('is_published', 'is_pinned')
    search_fields = ('title', 'content')
