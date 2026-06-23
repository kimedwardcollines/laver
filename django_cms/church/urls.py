"""
URL configuration for church app
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('ministries/', views.MinistriesView.as_view(), name='ministries'),
    path('ministries/<slug:slug>/', views.MinistryDetailView.as_view(), name='ministry_detail'),
    path('events/', views.EventsView.as_view(), name='events'),
    path('events/<slug:slug>/', views.EventDetailView.as_view(), name='event_detail'),
    path('sermons/', views.SermonsView.as_view(), name='sermons'),
    path('sermons/<slug:slug>/', views.SermonDetailView.as_view(), name='sermon_detail'),
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/submit/', views.contact_form_submit, name='contact_submit'),
    path('prayer-request/', views.PrayerRequestView.as_view(), name='prayer_request'),
    path('prayer-request/submit/', views.prayer_request_submit, name='prayer_request_submit'),
    path('give/', views.GiveView.as_view(), name='give'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]
