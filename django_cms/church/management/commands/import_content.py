"""
Management command to import existing church content into database models.
Run: python manage.py import_content
"""
from django.core.management.base import BaseCommand
from church.models import (
    ChurchInfo, Leadership, Ministry, ServiceTime, 
    Event, Sermon, Testimonial, GivingInfo
)


class Command(BaseCommand):
    help = 'Import existing church content into database models'

    def handle(self, *args, **options):
        self.stdout.write('Starting content import...\n')
        
        # Import Church Info
        self.import_church_info()
        
        # Import Leadership
        self.import_leadership()
        
        # Import Ministries
        self.import_ministries()
        
        # Import Service Times
        self.import_service_times()
        
        # Import Events
        self.import_events()
        
        # Import Sermons
        self.import_sermons()
        
        # Import Testimonials
        self.import_testimonials()
        
        # Import Giving Info
        self.import_giving_info()
        
        self.stdout.write(self.style.SUCCESS('\n✅ All content imported successfully!'))

    def import_church_info(self):
        if ChurchInfo.objects.exists():
            self.stdout.write(f'⚠️  ChurchInfo already exists, skipping...')
            return
            
        ChurchInfo.objects.create(
            name='Laver Transformation Ministries',
            mission='To transform lives through the power of God\'s Word, creating a community where people from all walks of life can experience spiritual growth, find purpose, and discover their God-given potential.',
            vision='To be a leading force for positive change in Wamala and beyond, raising up generations of believers who are rooted in faith, equipped for service, and committed to making a difference in their communities.',
            history='Laver Transformation Ministries was established with a clear vision: to be a beacon of hope and transformation in the Wamala community. What started as a small gathering of believers has grown into a vibrant community dedicated to spreading God\'s love and transforming lives through the power of His Word. Located along Wamala Katoke Road, our church has become a spiritual home for families, youth, and individuals seeking a deeper relationship with God. We believe in the power of community, worship, and service to bring about lasting transformation in people\'s lives.',
            address='Wamala, along Wamala Katoke Road, Central Uganda',
            phone='+256 XXX XXX XXX',
            email='info@lavertransformation.org',
            welcome_message='Welcome to Laver Transformation Ministries! We are thrilled to have you join us. Whether you are a first-time visitor or a returning member, you are family here. May you experience the love of God and find spiritual growth during your time with us.',
            senior_pastor_name='Pastor Milly Nankabirwa',
            senior_pastor_title='Senior Pastor',
            facebook='',
            instagram='',
            youtube='https://youtube.com/@lavertransformationchurch',
            whatsapp='',
        )
        self.stdout.write(f'✅ ChurchInfo created')

    def import_leadership(self):
        if Leadership.objects.exists():
            self.stdout.write(f'⚠️  Leadership already exists ({Leadership.objects.count()} records), skipping...')
            return
        
        leaders = [
            {
                'name': 'Pastor Milly Nankabirwa',
                'position': 'Senior Pastor',
                'bio': 'Leading our congregation with wisdom, compassion, and a heart for transformation. Pastor Milly has been serving the Lord for over 15 years and has a passion for seeing lives changed through God\'s Word.',
                'email': '',
                'phone': '',
                'display_order': 1,
                'is_active': True,
            },
            {
                'name': 'Youth Pastor',
                'position': 'Youth Ministry Leader',
                'bio': 'Dedicated to empowering and mentoring the next generation. Our Youth Pastor works closely with young people to help them grow in faith and discover their purpose.',
                'email': '',
                'phone': '',
                'display_order': 2,
                'is_active': True,
            },
            {
                'name': 'Pastor Emmanuel',
                'position': 'Worship Pastor',
                'bio': 'Leading our congregation in heartfelt worship and praise. Pastor Emmanuel oversees our worship ministry and music programs.',
                'email': '',
                'phone': '',
                'display_order': 3,
                'is_active': True,
            },
        ]
        
        for leader in leaders:
            Leadership.objects.create(**leader)
        self.stdout.write(f'✅ Leadership created ({len(leaders)} leaders)')

    def import_ministries(self):
        if Ministry.objects.exists():
            self.stdout.write(f'⚠️  Ministries already exists ({Ministry.objects.count()} records), skipping...')
            return
        
        # Get the Senior Pastor for leading some ministries
        pastor = Leadership.objects.filter(position='Senior Pastor').first()
        
        ministries = [
            {
                'name': 'Youth Ministry',
                'slug': 'youth-ministry',
                'description': '<p>Our Youth Ministry is dedicated to raising up young people who are rooted in faith and ready to impact their generation. Through worship, fellowship, and discipleship, we help youth discover their God-given potential.</p><p><strong>Features:</strong></p><ul><li>Weekly Youth Service (Sunday 2:00 PM)</li><li>Youth Bible Study</li><li>Leadership Training</li><li>Summer Camps & Retreats</li><li>Community Outreach</li></ul>',
                'icon': 'fa-users',
                'display_order': 1,
                'is_active': True,
            },
            {
                'name': 'Children\'s Ministry',
                'slug': 'childrens-ministry',
                'description': '<p>Our Children\'s Ministry provides a safe, fun, and biblically grounded environment for children to grow in their faith. We believe it\'s never too early to start a journey with Jesus.</p><p><strong>Features:</strong></p><ul><li>Sunday School</li><li>Children\'s Church</li><li>Vacation Bible School</li><li>Children\'s Choir</li><li>Youth Mentorship</li></ul>',
                'icon': 'fa-child',
                'display_order': 2,
                'is_active': True,
            },
            {
                'name': 'Worship Ministry',
                'slug': 'worship-ministry',
                'description': '<p>Our Worship Ministry creates an atmosphere where people can encounter God\'s presence through praise and worship. We use music, song, and creative expression to glorify God and lead others into worship.</p><p><strong>Features:</strong></p><ul><li>Main Worship Team</li><li>Choir Ministry</li><li>Instrumental Team</li><li>Dance Ministry</li><li>Sound & Media Team</li></ul>',
                'icon': 'fa-music',
                'display_order': 3,
                'is_active': True,
            },
            {
                'name': 'Prayer Ministry',
                'slug': 'prayer-ministry',
                'description': '<p>Our Prayer Ministry exists to intercede for the church, community, and world. We believe in the power of prayer and its ability to bring about transformation and breakthrough.</p><p><strong>Features:</strong></p><ul><li>Weekly Prayer Meeting (Friday 6:00 PM)</li><li>Prayer Chain Network</li><li>Morning Prayer Sessions</li><li>Prayer Walks</li><li>Intercessory Prayer Team</li></ul>',
                'icon': 'fa-pray',
                'display_order': 4,
                'is_active': True,
            },
            {
                'name': 'Community Outreach',
                'slug': 'community-outreach',
                'description': '<p>Our Outreach Ministry is committed to meeting the physical and spiritual needs of our community. We believe in being the hands and feet of Jesus by serving those around us.</p><p><strong>Features:</strong></p><ul><li>Health Camps</li><li>Food Drives</li><li>School Support Programs</li><li>Evangelism & Discipleship</li><li>Emergency Relief</li></ul>',
                'icon': 'fa-hands-helping',
                'display_order': 5,
                'is_active': True,
            },
            {
                'name': 'Women\'s Ministry',
                'slug': 'womens-ministry',
                'description': '<p>Our Women\'s Ministry creates a space for women to grow in faith, build meaningful relationships, and discover their God-given purpose. We encourage women of all ages to connect and encourage one another.</p><p><strong>Features:</strong></p><ul><li>Women\'s Fellowship</li><li>Bible Study Groups</li><li>Mentorship Program</li><li>Women\'s Retreats</li><li>Service Projects</li></ul>',
                'icon': 'fa-female',
                'display_order': 6,
                'is_active': True,
            },
            {
                'name': 'Men\'s Ministry',
                'slug': 'mens-ministry',
                'description': '<p>Our Men\'s Ministry challenges men to grow in their faith, lead their families with integrity, and serve the church and community with excellence. We create spaces for honest fellowship and spiritual growth.</p><p><strong>Features:</strong></p><ul><li>Men\'s Fellowship</li><li>Bible Study Groups</li><li>Mentorship & Discipleship</li><li>Men\'s Retreats</li><li>Service Projects</li></ul>',
                'icon': 'fa-male',
                'display_order': 7,
                'is_active': True,
            },
            {
                'name': 'Ushers & Hospitality',
                'slug': 'ushers-hospitality',
                'description': '<p>Our Ushers & Hospitality Ministry ensures everyone who walks through our doors feels welcomed and cared for. We take pride in creating a warm, hospitable environment for all.</p><p><strong>Features:</strong></p><ul><li>Sunday Service Ushers</li><li>Welcome Center</li><li>New Visitor Follow-up</li><li>Refreshments Team</li><li>Parking Team</li></ul>',
                'icon': 'fa-door-open',
                'display_order': 8,
                'is_active': True,
            },
        ]
        
        for ministry in ministries:
            Ministry.objects.create(**ministry)
        self.stdout.write(f'✅ Ministries created ({len(ministries)} ministries)')

    def import_service_times(self):
        if ServiceTime.objects.exists():
            self.stdout.write(f'⚠️  ServiceTimes already exists ({ServiceTime.objects.count()} records), skipping...')
            return
        
        services = [
            {'name': 'Sunday Service', 'day': 'Sunday', 'time': '9:00 AM', 'description': 'Main weekly worship service', 'display_order': 1, 'is_active': True},
            {'name': 'Youth Service', 'day': 'Sunday', 'time': '2:00 PM', 'description': 'Youth-focused worship and teaching', 'display_order': 2, 'is_active': True},
            {'name': 'Bible Study', 'day': 'Wednesday', 'time': '7:00 PM', 'description': 'Midweek Bible study and prayer', 'display_order': 3, 'is_active': True},
            {'name': 'Prayer Meeting', 'day': 'Friday', 'time': '6:00 PM', 'description': 'Weekly prayer meeting', 'display_order': 4, 'is_active': True},
            {'name': 'Morning Prayer', 'day': 'Daily', 'time': '6:00 AM', 'description': 'Daily morning prayer session (Mon-Sat)', 'display_order': 5, 'is_active': True},
        ]
        
        for service in services:
            ServiceTime.objects.create(**service)
        self.stdout.write(f'✅ Service Times created ({len(services)} services)')

    def import_events(self):
        if Event.objects.exists():
            self.stdout.write(f'⚠️  Events already exists ({Event.objects.count()} records), skipping...')
            return
        
        from datetime import datetime
        
        events = [
            {'title': 'Youth Revival Service', 'slug': 'youth-revival-service', 'description': '<p>Join us for a powerful evening of worship, prayer, and word as our youth come together to seek God\'s face and experience revival in their lives.</p>', 'start_date': datetime(2024, 10, 20, 14, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': True},
            {'title': 'Community Health Camp', 'slug': 'community-health-camp', 'description': '<p>Free health screenings, consultations, and health education for the Wamala community. Partnering with local health professionals to serve our neighbors.</p>', 'start_date': datetime(2024, 10, 26, 8, 0), 'location': 'Church Grounds', 'is_published': True, 'is_featured': True},
            {'title': 'Thanksgiving Sunday', 'slug': 'thanksgiving-sunday', 'description': '<p>A special service to give thanks to God for His faithfulness and blessings. Bring your thanksgiving offerings and testimonies.</p>', 'start_date': datetime(2024, 11, 3, 9, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': False},
            {'title': 'Couples Fellowship', 'slug': 'couples-fellowship', 'description': '<p>An evening for married couples to connect, learn, and strengthen their relationships through God\'s word.</p>', 'start_date': datetime(2024, 11, 10, 16, 0), 'location': 'Fellowship Hall', 'is_published': True, 'is_featured': False},
            {'title': 'Leadership Conference', 'slug': 'leadership-conference', 'description': '<p>A one-day conference for church leaders focusing on servant leadership and equipping believers for ministry.</p>', 'start_date': datetime(2024, 11, 24, 8, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': True},
            {'title': 'Christmas Carol Service', 'slug': 'christmas-carol-service', 'description': '<p>Celebrate the birth of Christ with carols, worship, and the true meaning of Christmas. Bring your family and friends!</p>', 'start_date': datetime(2024, 12, 15, 17, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': True},
            {'title': 'New Year Prayer', 'slug': 'new-year-prayer', 'description': '<p>Start the new year in prayer! Join us for an early morning prayer session to seek God\'s guidance and blessing for the year ahead.</p>', 'start_date': datetime(2025, 1, 8, 6, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': False},
            {'title': 'Youth Camp', 'slug': 'youth-camp', 'description': '<p>An exciting camp experience for youth with worship, teaching, team building, and fun activities.</p>', 'start_date': datetime(2025, 1, 15, 8, 0), 'location': 'Camp Ground', 'is_published': True, 'is_featured': True},
            {'title': 'Church Anniversary', 'slug': 'church-anniversary', 'description': '<p>Celebrating another year of God\'s faithfulness! Join us for a special anniversary service and celebration.</p>', 'start_date': datetime(2025, 2, 1, 9, 0), 'location': 'Main Sanctuary', 'is_published': True, 'is_featured': True},
        ]
        
        for event in events:
            Event.objects.create(**event)
        self.stdout.write(f'✅ Events created ({len(events)} events)')

    def import_sermons(self):
        if Sermon.objects.exists():
            self.stdout.write(f'⚠️  Sermons already exists ({Sermon.objects.count()} records), skipping...')
            return
        
        from datetime import date
        
        pastor = Leadership.objects.filter(position='Senior Pastor').first()
        youth_pastor = Leadership.objects.filter(position='Youth Ministry Leader').first()
        worship_pastor = Leadership.objects.filter(position='Worship Pastor').first()
        
        sermons = [
            {
                'title': 'The Power of Faith',
                'slug': 'the-power-of-faith',
                'speaker': pastor,
                'date_preached': date(2024, 10, 15),
                'description': '<p><strong>Series:</strong> Walking in Faith Series</p><p><strong>Scripture:</strong> Hebrews 11:1</p><p>Discover how faith can move mountains and transform your life as we explore the heroes of faith in Scripture.</p><p><strong>Duration:</strong> 45 min</p>',
                'is_published': True,
                'is_featured': True,
            },
            {
                'title': 'Walking in God\'s Purpose',
                'slug': 'walking-in-gods-purpose',
                'speaker': pastor,
                'date_preached': date(2024, 10, 8),
                'description': '<p><strong>Series:</strong> Discovering Your Destiny Series</p><p><strong>Scripture:</strong> Jeremiah 29:11</p><p>Understanding God\'s plan for your life and how to align with His perfect will for your future.</p><p><strong>Duration:</strong> 52 min</p>',
                'is_published': True,
                'is_featured': True,
            },
            {
                'title': 'The Love of Christ',
                'slug': 'the-love-of-christ',
                'speaker': youth_pastor,
                'date_preached': date(2024, 10, 1),
                'description': '<p><strong>Series:</strong> Deepening Your Love Series</p><p><strong>Scripture:</strong> John 3:16</p><p>Exploring the depth of God\'s love and what it means for our daily lives as believers.</p><p><strong>Duration:</strong> 48 min</p>',
                'is_published': True,
                'is_featured': False,
            },
            {
                'title': 'Overcoming Trials',
                'slug': 'overcoming-trials',
                'speaker': worship_pastor,
                'date_preached': date(2024, 9, 24),
                'description': '<p><strong>Series:</strong> Victory in Christ Series</p><p><strong>Scripture:</strong> James 1:2-4</p><p>Learning to see trials as opportunities for growth and developing perseverance through faith.</p><p><strong>Duration:</strong> 55 min</p>',
                'is_published': True,
                'is_featured': False,
            },
            {
                'title': 'Prayer That Moves Heaven',
                'slug': 'prayer-that-moves-heaven',
                'speaker': pastor,
                'date_preached': date(2024, 9, 17),
                'description': '<p><strong>Series:</strong> Power of Prayer Series</p><p><strong>Scripture:</strong> Matthew 7:7-11</p><p>Understanding the power of persistent prayer and how to pray effectively for breakthrough.</p><p><strong>Duration:</strong> 50 min</p>',
                'is_published': True,
                'is_featured': False,
            },
            {
                'title': 'Living as Disciples',
                'slug': 'living-as-disciples',
                'speaker': youth_pastor,
                'date_preached': date(2024, 9, 10),
                'description': '<p><strong>Series:</strong> Discipleship Series</p><p><strong>Scripture:</strong> Matthew 28:19-20</p><p>What it means to be a disciple of Christ and how to grow in your Christian walk.</p><p><strong>Duration:</strong> 47 min</p>',
                'is_published': True,
                'is_featured': False,
            },
        ]
        
        for sermon in sermons:
            Sermon.objects.create(**sermon)
        self.stdout.write(f'✅ Sermons created ({len(sermons)} sermons)')

    def import_testimonials(self):
        if Testimonial.objects.exists():
            self.stdout.write(f'⚠️  Testimonials already exists ({Testimonial.objects.count()} records), skipping...')
            return
        
        testimonials = [
            {
                'name': 'Sarah Namuli',
                'testimony': 'Laver Transformation Ministries changed my life. The community here feels like family, and I\'ve grown spiritually in ways I never imagined possible.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'David Okello',
                'testimony': 'As a youth, I found a place where I belong. The youth ministry has helped me discover my purpose and grow closer to God.',
                'is_approved': True,
                'is_featured': True,
            },
            {
                'name': 'Grace Akello',
                'testimony': 'I visited for the first time while passing through Wamala. The welcome was genuine, and I felt the presence of God in the service.',
                'is_approved': True,
                'is_featured': True,
            },
        ]
        
        for testimonial in testimonials:
            Testimonial.objects.create(**testimonial)
        self.stdout.write(f'✅ Testimonials created ({len(testimonials)} testimonials)')

    def import_giving_info(self):
        if GivingInfo.objects.exists():
            self.stdout.write(f'⚠️  GivingInfo already exists, skipping...')
            return
        
        GivingInfo.objects.create(
            title='Support Our Ministry',
            description='<p>Your generous giving helps us continue our mission to transform lives through God\'s Word. We believe in being faithful stewards of every resource God provides.</p><p><strong>Biblical Basis:</strong> "Each of you should give what you have decided in your heart to give, not reluctantly or under compulsion, for God loves a cheerful giver." — 2 Corinthians 9:7</p>',
            mtn_mobile='XXXXXXXXXX',
            airtel_mobile='XXXXXXXXXX',
            bank_name='XXXXXXXXXXXXXXXXXXX',
            bank_account_name='Laver Transformation Ministries',
            bank_account_number='XXXXXXXXXXXXXXXXXXX',
            bank_swift_code='XXXXXXXXXXXXXXXXXXX',
            is_active=True,
        )
        self.stdout.write(f'✅ GivingInfo created')
