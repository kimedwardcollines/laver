"""
Dashboard URL configuration
"""
from django.urls import path
from . import dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
    path('login/', dashboard_views.login_view, name='dashboard_login'),
    path('logout/', dashboard_views.logout_view, name='dashboard_logout'),
    
    # Church Info
    path('church-info/', dashboard_views.church_info, name='church_info'),
    
    # Leadership
    path('leadership/', dashboard_views.leadership_list, name='leadership_list'),
    path('leadership/add/', dashboard_views.leadership_create, name='leadership_add'),
    path('leadership/<int:pk>/edit/', dashboard_views.leadership_edit, name='leadership_edit'),
    path('leadership/<int:pk>/delete/', dashboard_views.leadership_delete, name='leadership_delete'),
    
    # Ministries
    path('ministries/', dashboard_views.ministries_list, name='ministries_list'),
    path('ministries/add/', dashboard_views.ministry_create, name='ministry_add'),
    path('ministries/<int:pk>/edit/', dashboard_views.ministry_edit, name='ministry_edit'),
    path('ministries/<int:pk>/delete/', dashboard_views.ministry_delete, name='ministry_delete'),
    
    # Service Times
    path('service-times/', dashboard_views.service_times_list, name='service_times_list'),
    path('service-times/add/', dashboard_views.service_time_create, name='service_time_add'),
    path('service-times/<int:pk>/edit/', dashboard_views.service_time_edit, name='service_time_edit'),
    path('service-times/<int:pk>/delete/', dashboard_views.service_time_delete, name='service_time_delete'),
    
    # Events
    path('events/', dashboard_views.events_list, name='dashboard_events'),
    path('events/add/', dashboard_views.event_create, name='event_add'),
    path('events/<int:pk>/edit/', dashboard_views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', dashboard_views.event_delete, name='event_delete'),
    
    # Sermons
    path('sermons/', dashboard_views.sermons_list, name='dashboard_sermons'),
    path('sermons/add/', dashboard_views.sermon_create, name='sermon_add'),
    path('sermons/<int:pk>/edit/', dashboard_views.sermon_edit, name='sermon_edit'),
    path('sermons/<int:pk>/delete/', dashboard_views.sermon_delete, name='sermon_delete'),
    
    # Gallery
    path('gallery/', dashboard_views.gallery_list, name='dashboard_gallery'),
    path('gallery/add/', dashboard_views.gallery_image_create, name='gallery_add'),
    path('gallery/<int:pk>/delete/', dashboard_views.gallery_image_delete, name='gallery_delete'),
    
    # Testimonials
    path('testimonials/', dashboard_views.testimonials_list, name='testimonials_list'),
    path('testimonials/add/', dashboard_views.testimonial_create, name='testimonial_add'),
    path('testimonials/<int:pk>/edit/', dashboard_views.testimonial_edit, name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', dashboard_views.testimonial_delete, name='testimonial_delete'),
    
    # Announcements
    path('announcements/', dashboard_views.announcements_list, name='announcements_list'),
    path('announcements/add/', dashboard_views.announcement_create, name='announcement_add'),
    path('announcements/<int:pk>/edit/', dashboard_views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', dashboard_views.announcement_delete, name='announcement_delete'),
    
    # Prayer Requests
    path('prayer-requests/', dashboard_views.prayer_requests_list, name='prayer_requests_list'),
    path('prayer-requests/<int:pk>/update/', dashboard_views.prayer_request_update, name='prayer_request_update'),
    
    # Newsletter
    path('newsletter/', dashboard_views.newsletter_list, name='newsletter_list'),
    
    # Messages
    path('messages/', dashboard_views.messages_list, name='messages_list'),
    path('messages/<int:pk>/', dashboard_views.message_detail, name='message_detail'),
    
    # Giving
    path('giving/', dashboard_views.giving_info, name='giving_info'),
]
