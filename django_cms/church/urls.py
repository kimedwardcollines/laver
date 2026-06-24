from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ministries/', views.ministries, name='ministries'),
    path('ministries/<slug:slug>/', views.ministry_detail, name='ministry_detail'),
    path('sermons/', views.sermons, name='sermons'),
    path('sermons/<slug:slug>/', views.sermon_detail, name='sermon_detail'),
    path('events/', views.events, name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('give/', views.give, name='give'),
    path('prayer-request/', views.prayer_request, name='prayer_request'),
]
