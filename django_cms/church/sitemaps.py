"""
Sitemaps for SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'ministries', 'events', 'sermons', 'gallery', 'contact', 'prayer_request', 'give']
    
    def location(self, item):
        return reverse(item)
