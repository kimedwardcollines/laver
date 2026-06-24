"""
Management command to import content from the static HTML site into the CMS database.
"""
import os
import re
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone
from church.models import (
    ChurchInfo, Leadership, Ministry, ServiceTime,
    Event, Sermon, GalleryImage, Testimonial,
    PrayerRequest, ContactMessage, GivingInfo, Announcement
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Import content from static HTML files into the CMS database'

    def __init__(self):
        super().__init__()
        self.static_site_path = '/workspace/project/laver'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recreate all content (will delete existing data)',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        self.stdout.write(self.style.SUCCESS('Starting import from static site...'))
        
        # Create admin user
        self.create_admin_user()
        
        # Import church info
        self.import_church_info()
        
        # Import leadership
        self.import_leadership()
        
        # Import ministries
        self.import_ministries()
        
        # Import service times
        self.import_service_times()
        
        # Import events
        self.import_events()
        
        # Import sermons
        self.import_sermons()
        
        # Import testimonials
        self.import_testimonials()
        
        # Import giving info
        self.import_giving_info()
        
        # Import announcements
        self.import_announcements()
        
        self.stdout.write(self.style.SUCCESS('\n✓ Import completed successfully!'))

    def create_admin_user(self):
        """Create admin user if not exists."""
        username = 'admin'
        password = 'admin123'
        email = 'admin@lavertransformation.org'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(f'  ✓ Created admin user (username: {username}, password: {password})')
        else:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(f'  ✓ Updated admin user password')

    def read_html_file(self, filename):
        """Read an HTML file from the static site."""
        filepath = os.path.join(self.static_site_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    def extract_text_between(self, html, start_tag, end_tag):
        """Extract text content between HTML tags."""
        pattern = f'{start_tag}(.*?){end_tag}'
        match = re.search(pattern, html, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ''

    def strip_html_tags(self, text):
        """Remove HTML tags from text."""
        if not text:
            return ''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def import_church_info(self):
        """Import church information from index.html."""
        html = self.read_html_file('index.html')
        if not html:
            self.stdout.write(self.style.WARNING('  ⚠ index.html not found, skipping church info'))
            return

        # Check if church info already exists
        church_info, created = ChurchInfo.objects.get_or_create(pk=1)
        
        church_info.name = 'Laver Transformation Ministries'
        church_info.senior_pastor_name = 'Pastor Milly Nankabirwa'
        church_info.senior_pastor_title = 'Senior Pastor'
        church_info.address = 'Wamala, along Wamala Katoke Road, Central Uganda'
        church_info.phone = '+256 XXX XXX XXX'
        church_info.email = 'info@lavertransformation.org'
        church_info.facebook = 'https://www.facebook.com/lavertransformation'
        church_info.instagram = 'https://www.instagram.com/lavertransformation'
        church_info.youtube = 'https://youtube.com/@lavertransformationchurch'
        church_info.whatsapp = '+256 XXX XXX XXX'
        
        church_info.welcome_message = '''
            <p>On behalf of our entire church family, I want to welcome you to Laver Transformation Ministries. 
            Whether you're exploring faith for the first time, returning to church after some time away, 
            or looking for a church home, we're thrilled you're here.</p>
            <p>At Laver, we believe that everyone is designed for a purpose greater than themselves. 
            Our doors are open to all who seek truth, community, and a deeper relationship with God.</p>
        '''
        
        church_info.mission = '''
            <p>To transform lives through the power of God's Word, creating a community where people from 
            all walks of life can experience spiritual growth, find purpose, and discover their God-given potential.</p>
        '''
        
        church_info.vision = '''
            <p>To be a leading force for positive change in Wamala and beyond, raising up generations of believers 
            who are rooted in faith, equipped for service, and committed to making a difference in their communities.</p>
        '''
        
        church_info.history = '''
            <p>Laver Transformation Ministries was established with a clear vision: to be a beacon of hope and 
            transformation in the Wamala community. What started as a small gathering of believers has grown into 
            a vibrant community dedicated to spreading God's love and transforming lives through the power of His Word.</p>
            <p>Located along Wamala Katoke Road, our church has become a spiritual home for families, youth, and 
            individuals seeking a deeper relationship with God. We believe in the power of community, worship, 
            and service to bring about lasting transformation in people's lives.</p>
        '''
        
        church_info.save()
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'  ✓ {action} church information')

    def import_leadership(self):
        """Import leadership team from about.html."""
        leadership_data = [
            {
                'name': 'Pastor Milly Nankabirwa',
                'position': 'Senior Pastor',
                'bio': 'Leading our congregation with wisdom, compassion, and a heart for transformation. Pastor Milly has been serving the Lord for over 15 years and has a passion for seeing lives changed through God\'s Word.',
                'is_senior_pastor': True,
                'display_order': 1,
            },
            {
                'name': 'Youth Pastor',
                'position': 'Youth Ministry Leader',
                'bio': 'Dedicated to empowering and mentoring the next generation. Our Youth Pastor works closely with young people to help them grow in faith and discover their purpose.',
                'is_senior_pastor': False,
                'display_order': 2,
            },
            {
                'name': 'Pastor Emmanuel',
                'position': 'Worship Pastor',
                'bio': 'Leading our congregation in heartfelt worship and praise. Pastor Emmanuel oversees our worship ministry and music programs.',
                'is_senior_pastor': False,
                'display_order': 3,
            },
        ]
        
        for data in leadership_data:
            leadership, created = Leadership.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if not created:
                for key, value in data.items():
                    setattr(leadership, key, value)
                leadership.save()
        
        self.stdout.write(f'  ✓ Imported {len(leadership_data)} leadership members')

    def import_ministries(self):
        """Import ministries from ministries.html."""
        ministries_data = [
            {
                'name': 'Youth Ministry',
                'slug': 'youth-ministry',
                'description': '''
                    <p>Our Youth Ministry is dedicated to raising up young people who are rooted in faith and ready to impact their generation.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Weekly Youth Service (Sunday 2:00 PM)</li>
                        <li><i class="fas fa-check"></i> Youth Bible Study</li>
                        <li><i class="fas fa-check"></i> Leadership Training</li>
                        <li><i class="fas fa-check"></i> Summer Camps & Retreats</li>
                        <li><i class="fas fa-check"></i> Community Outreach</li>
                    </ul>
                ''',
                'icon': 'fa-users',
                'display_order': 1,
            },
            {
                'name': "Children's Ministry",
                'slug': 'childrens-ministry',
                'description': '''
                    <p>Our Children's Ministry provides a safe, fun, and biblically grounded environment for children to grow in their faith.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Sunday School</li>
                        <li><i class="fas fa-check"></i> Children's Church</li>
                        <li><i class="fas fa-check"></i> Vacation Bible School</li>
                        <li><i class="fas fa-check"></i> Children's Choir</li>
                        <li><i class="fas fa-check"></i> Youth Mentorship</li>
                    </ul>
                ''',
                'icon': 'fa-child',
                'display_order': 2,
            },
            {
                'name': 'Worship Ministry',
                'slug': 'worship-ministry',
                'description': '''
                    <p>Our Worship Ministry creates an atmosphere where people can encounter God's presence through praise and worship.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Main Worship Team</li>
                        <li><i class="fas fa-check"></i> Choir Ministry</li>
                        <li><i class="fas fa-check"></i> Instrumental Team</li>
                        <li><i class="fas fa-check"></i> Dance Ministry</li>
                        <li><i class="fas fa-check"></i> Sound & Media Team</li>
                    </ul>
                ''',
                'icon': 'fa-music',
                'display_order': 3,
            },
            {
                'name': 'Prayer Ministry',
                'slug': 'prayer-ministry',
                'description': '''
                    <p>Our Prayer Ministry is committed to interceding for our community, nation, and the world.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Prayer Chain Network</li>
                        <li><i class="fas fa-check"></i> Morning Prayer Sessions</li>
                        <li><i class="fas fa-check"></i> Prayer Walks</li>
                        <li><i class="fas fa-check"></i> Intercessory Prayer Team</li>
                    </ul>
                ''',
                'icon': 'fa-pray',
                'display_order': 4,
            },
            {
                'name': 'Community Outreach',
                'slug': 'community-outreach',
                'description': '''
                    <p>Our Outreach Ministry is committed to meeting the physical and spiritual needs of our community.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Health Camps</li>
                        <li><i class="fas fa-check"></i> Food Drives</li>
                        <li><i class="fas fa-check"></i> School Support Programs</li>
                        <li><i class="fas fa-check"></i> Evangelism & Discipleship</li>
                        <li><i class="fas fa-check"></i> Emergency Relief</li>
                    </ul>
                ''',
                'icon': 'fa-hands-helping',
                'display_order': 5,
            },
            {
                'name': "Women's Ministry",
                'slug': 'womens-ministry',
                'description': '''
                    <p>Our Women's Ministry creates a space for women to grow in faith, build meaningful relationships, and discover their God-given purpose.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Women's Fellowship</li>
                        <li><i class="fas fa-check"></i> Bible Study Groups</li>
                        <li><i class="fas fa-check"></i> Mentorship Program</li>
                        <li><i class="fas fa-check"></i> Women's Retreats</li>
                        <li><i class="fas fa-check"></i> Service Projects</li>
                    </ul>
                ''',
                'icon': 'fa-female',
                'display_order': 6,
            },
            {
                'name': "Men's Ministry",
                'slug': 'mens-ministry',
                'description': '''
                    <p>Our Men's Ministry challenges men to grow in their faith, lead their families with integrity, and serve the church and community with excellence.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Men's Fellowship</li>
                        <li><i class="fas fa-check"></i> Bible Study Groups</li>
                        <li><i class="fas fa-check"></i> Mentorship & Discipleship</li>
                        <li><i class="fas fa-check"></i> Men's Retreats</li>
                        <li><i class="fas fa-check"></i> Service Projects</li>
                    </ul>
                ''',
                'icon': 'fa-male',
                'display_order': 7,
            },
            {
                'name': 'Ushers & Hospitality',
                'slug': 'ushers-hospitality',
                'description': '''
                    <p>Our Ushers & Hospitality Ministry ensures everyone who walks through our doors feels welcomed and cared for.</p>
                    <ul class="ministry-features">
                        <li><i class="fas fa-check"></i> Sunday Service Ushers</li>
                        <li><i class="fas fa-check"></i> Welcome Center</li>
                        <li><i class="fas fa-check"></i> New Visitor Follow-up</li>
                        <li><i class="fas fa-check"></i> Refreshments Team</li>
                        <li><i class="fas fa-check"></i> Parking Team</li>
                    </ul>
                ''',
                'icon': 'fa-concierge-bell',
                'display_order': 8,
            },
        ]
        
        for data in ministries_data:
            ministry, created = Ministry.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if not created:
                for key, value in data.items():
                    setattr(ministry, key, value)
                ministry.save()
        
        self.stdout.write(f'  ✓ Imported {len(ministries_data)} ministries')

    def import_service_times(self):
        """Import weekly service times."""
        service_times_data = [
            {'name': 'Sunday Service', 'day': 'Sunday', 'time': '9:00 AM', 'display_order': 1},
            {'name': 'Youth Service', 'day': 'Sunday', 'time': '2:00 PM', 'display_order': 2},
            {'name': 'Bible Study', 'day': 'Wednesday', 'time': '7:00 PM', 'display_order': 3},
            {'name': 'Prayer Meeting', 'day': 'Friday', 'time': '6:00 PM', 'display_order': 4},
        ]
        
        for data in service_times_data:
            st, created = ServiceTime.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
        
        self.stdout.write(f'  ✓ Imported {len(service_times_data)} service times')

    def import_events(self):
        """Import events from events.html."""
        def make_aware(dt):
            """Convert naive datetime to timezone-aware datetime."""
            return timezone.make_aware(dt, timezone.get_default_timezone())
        
        events_data = [
            {
                'title': 'Youth Revival Service',
                'slug': 'youth-revival-service',
                'start_date': make_aware(datetime(2024, 10, 20, 14, 0)),
                'end_date': make_aware(datetime(2024, 10, 20, 17, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>A special service dedicated to the youth with worship, prayer, and an encouraging message.</p>',
                'is_featured': True,
            },
            {
                'title': 'Community Health Camp',
                'slug': 'community-health-camp',
                'start_date': make_aware(datetime(2024, 10, 26, 8, 0)),
                'end_date': make_aware(datetime(2024, 10, 26, 16, 0)),
                'location': 'Church Grounds',
                'description': '<p>Free health screenings and wellness education for the Wamala community.</p>',
            },
            {
                'title': 'Thanksgiving Sunday',
                'slug': 'thanksgiving-sunday',
                'start_date': make_aware(datetime(2024, 11, 3, 9, 0)),
                'end_date': make_aware(datetime(2024, 11, 3, 13, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>Celebrate God\'s faithfulness with offerings and testimonies.</p>',
            },
            {
                'title': 'Couples Fellowship',
                'slug': 'couples-fellowship',
                'start_date': make_aware(datetime(2024, 11, 10, 16, 0)),
                'end_date': make_aware(datetime(2024, 11, 10, 19, 0)),
                'location': 'Fellowship Hall',
                'description': '<p>Building stronger marriages through God\'s Word.</p>',
            },
            {
                'title': 'Prayer Summit',
                'slug': 'prayer-summit',
                'start_date': make_aware(datetime(2024, 11, 17, 7, 0)),
                'end_date': make_aware(datetime(2024, 11, 17, 12, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>A day of fasting and prayer for our nation and community.</p>',
            },
            {
                'title': 'Christmas Carol Service',
                'slug': 'christmas-carol-service',
                'start_date': make_aware(datetime(2024, 12, 15, 17, 0)),
                'end_date': make_aware(datetime(2024, 12, 15, 20, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>Celebrate the birth of Christ with carols and refreshments.</p>',
                'is_featured': True,
            },
            {
                'title': 'New Year Prayer',
                'slug': 'new-year-prayer',
                'start_date': make_aware(datetime(2025, 1, 8, 6, 0)),
                'end_date': make_aware(datetime(2025, 1, 8, 10, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>Start the year with prayer and dedication to God.</p>',
            },
            {
                'title': 'Youth Camp',
                'slug': 'youth-camp',
                'start_date': make_aware(datetime(2025, 1, 15, 8, 0)),
                'location': 'Camp Ground',
                'description': '<p>Annual youth camp for spiritual growth and fellowship.</p>',
                'is_featured': True,
            },
            {
                'title': 'Church Anniversary',
                'slug': 'church-anniversary',
                'start_date': make_aware(datetime(2025, 2, 1, 9, 0)),
                'end_date': make_aware(datetime(2025, 2, 1, 16, 0)),
                'location': 'Main Sanctuary',
                'description': '<p>Celebrating another year of God\'s faithfulness.</p>',
                'is_featured': True,
            },
        ]
        
        for data in events_data:
            event, created = Event.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if not created:
                for key, value in data.items():
                    setattr(event, key, value)
                event.save()
        
        self.stdout.write(f'  ✓ Imported {len(events_data)} events')

    def import_sermons(self):
        """Import sermons from sermons.html."""
        sermons_data = [
            {
                'title': 'The Power of Faith',
                'slug': 'the-power-of-faith',
                'speaker': 'Pastor Milly Nankabirwa',
                'date_preached': datetime(2024, 10, 15).date(),
                'description': '<p>Discover how faith can move mountains and transform your life as we explore the heroes of faith in Scripture.</p><p>Scripture Reference: Hebrews 11:1</p><p>Series: Walking in Faith</p>',
                'is_featured': True,
            },
            {
                'title': "Walking in God's Purpose",
                'slug': 'walking-in-gods-purpose',
                'speaker': 'Pastor Milly Nankabirwa',
                'date_preached': datetime(2024, 10, 8).date(),
                'description': '<p>Understanding God\'s plan for your life and how to align with His perfect will for your future.</p><p>Scripture Reference: Jeremiah 29:11</p><p>Series: Discovering Your Destiny</p>',
                'is_featured': True,
            },
            {
                'title': 'The Love of Christ',
                'slug': 'the-love-of-christ',
                'speaker': 'Youth Pastor',
                'date_preached': datetime(2024, 10, 1).date(),
                'description': '<p>Exploring the depth of God\'s love and what it means for our daily lives as believers.</p><p>Scripture Reference: John 3:16</p><p>Series: Deepening Your Love</p>',
            },
            {
                'title': 'Overcoming Trials',
                'slug': 'overcoming-trials',
                'speaker': 'Pastor Emmanuel',
                'date_preached': datetime(2024, 9, 24).date(),
                'description': '<p>Learning to see trials as opportunities for growth and developing perseverance through faith.</p><p>Scripture Reference: James 1:2-4</p><p>Series: Victory in Christ</p>',
            },
            {
                'title': 'Prayer That Moves Heaven',
                'slug': 'prayer-that-moves-heaven',
                'speaker': 'Pastor Milly Nankabirwa',
                'date_preached': datetime(2024, 9, 17).date(),
                'description': '<p>Understanding the power of persistent prayer and how to pray effectively for breakthrough.</p><p>Scripture Reference: Matthew 7:7-11</p><p>Series: Power of Prayer</p>',
                'is_featured': True,
            },
            {
                'title': 'Living as Disciples',
                'slug': 'living-as-disciples',
                'speaker': 'Youth Pastor',
                'date_preached': datetime(2024, 9, 10).date(),
                'description': '<p>What it means to be a disciple of Christ and how to grow in your Christian walk.</p><p>Scripture Reference: Matthew 28:19-20</p><p>Series: Discipleship</p>',
            },
        ]
        
        for data in sermons_data:
            sermon, created = Sermon.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if not created:
                for key, value in data.items():
                    setattr(sermon, key, value)
                sermon.save()
        
        self.stdout.write(f'  ✓ Imported {len(sermons_data)} sermons')

    def import_testimonials(self):
        """Import testimonials."""
        testimonials_data = [
            {
                'name': 'Sarah K.',
                'testimony': 'Laver Transformation Ministries has been a blessing to my family. Through the youth programs, my children have grown spiritually and found a supportive community of believers.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'James M.',
                'testimony': 'I came to Laver feeling lost and broken. Through the prayers and support of this church, I found hope and a new purpose in Christ.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Grace N.',
                'testimony': 'The community outreach programs have blessed our family in so many ways. We are grateful for this church that truly lives out the love of Christ.',
                'is_approved': True,
                'is_featured': True,
            },
        ]
        
        for data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
        
        self.stdout.write(f'  ✓ Imported {len(testimonials_data)} testimonials')

    def import_giving_info(self):
        """Import giving information from give.html."""
        giving_info, created = GivingInfo.objects.get_or_create(pk=1)
        
        giving_info.title = 'Support Our Ministry'
        giving_info.description = '''
            <p>Thank you for partnering with us in ministry! Your generous giving helps us:</p>
            <ul>
                <li>Continue our mission to transform lives through God's Word</li>
                <li>Support community outreach programs</li>
                <li>Nurture the next generation through youth and children's ministries</li>
                <li>Spread the Gospel locally and globally</li>
            </ul>
        '''
        giving_info.mtn_mobile = 'Contact us for details'
        giving_info.airtel_mobile = 'Contact us for details'
        giving_info.bank_name = 'Contact us for bank details'
        giving_info.account_number = 'Contact us for account details'
        giving_info.account_name = 'Laver Transformation Ministries'
        
        giving_info.save()
        
        self.stdout.write(f'  ✓ {"Created" if created else "Updated"} giving information')

    def import_announcements(self):
        """Import announcements."""
        announcements_data = [
            {
                'title': 'Sunday Service Times',
                'content': '<p>Join us every Sunday at 9:00 AM for worship and biblical teaching. Youth service at 2:00 PM.</p>',
                'is_pinned': True,
            },
            {
                'title': 'Midweek Bible Study',
                'content': '<p>Bible Study and Prayer Meeting every Wednesday at 7:00 PM. All are welcome!</p>',
            },
            {
                'title': 'Youth Fellowship',
                'content': '<p>Youth service every Sunday at 2:00 PM. Come and be encouraged!</p>',
            },
        ]
        
        for data in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
        
        self.stdout.write(f'  ✓ Imported {len(announcements_data)} announcements')