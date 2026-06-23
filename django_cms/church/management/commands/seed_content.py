from django.core.management.base import BaseCommand
from church.models import (
    ChurchInfo, Leadership, Ministry, ServiceTime, 
    Event, Sermon, Testimonial, GivingInfo
)
from django.utils import timezone
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed database with church content'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...\n')

        # Church Info
        if not ChurchInfo.objects.exists():
            ChurchInfo.objects.create(
                name='Laver Transformation Ministries',
                senior_pastor_name='Pastor Milly Nankabirwa',
                senior_pastor_title='Senior Pastor',
                address='Wamala, along Wamala Katoke Road, Central Uganda',
                phone='+256 XXX XXX XXX',
                phone_2='',
                email='info@lavertransformation.org',
                facebook='https://www.facebook.com/lavertransformationchurch',
                instagram='https://www.instagram.com/lavertransformationchurch',
                youtube='https://youtube.com/@lavertransformationchurch',
                whatsapp='+256 700 000 000',
                welcome_message='''Welcome to Laver Transformation Ministries! We are thrilled to have you join us. Whether you are a first-time visitor or a returning member, you are family here. May you experience the love of God and find spiritual growth during your time with us.''',
                mission='''To transform lives through the power of God's Word, creating a community where people from all walks of life can experience spiritual growth, find purpose, and discover their God-given potential.''',
                vision='''To be a leading force for positive change in Wamala and beyond, raising up generations of believers who are rooted in faith, equipped for service, and committed to making a difference in their communities.''',
                history='''Laver Transformation Ministries was established with a clear vision: to be a beacon of hope and transformation in the Wamala community. What started as a small gathering of believers has grown into a vibrant community dedicated to spreading God's love and transforming lives through the power of His Word. Located along Wamala Katoke Road, our church has become a spiritual home for families, youth, and individuals seeking a deeper relationship with God. We believe in the power of community, worship, and service to bring about lasting transformation in people's lives.''',
            )
            self.stdout.write(self.style.SUCCESS('✓ Church Info created'))
        else:
            self.stdout.write('✓ Church Info already exists')

        # Leadership
        if not Leadership.objects.exists():
            Leadership.objects.create(
                name='Pastor Milly Nankabirwa',
                position='Senior Pastor',
                bio='Leading our congregation with wisdom, compassion, and a heart for transformation. Pastor Milly has been serving the Lord for over 15 years and has a passion for seeing lives changed through God\'s Word.',
                is_active=True,
                is_senior_pastor=True,
            )
            Leadership.objects.create(
                name='Youth Pastor',
                position='Youth Ministry Leader',
                bio='Dedicated to empowering and mentoring the next generation. Our Youth Pastor works closely with young people to help them grow in faith and discover their purpose.',
                is_active=True,
            )
            Leadership.objects.create(
                name='Pastor Emmanuel',
                position='Worship Pastor',
                bio='Leading our congregation in heartfelt worship and praise. Pastor Emmanuel oversees our worship ministry and music programs.',
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS('✓ Leadership created'))
        else:
            self.stdout.write('✓ Leadership already exists')

        # Ministries
        if not Ministry.objects.exists():
            ministries_data = [
                ('Youth Ministry', 'fas fa-users', '''<p>Our Youth Ministry is dedicated to raising up young people who are rooted in faith and ready to impact their generation. Through worship, fellowship, and discipleship, we help youth discover their God-given potential.</p>
<p>We create an environment where young people can build lasting friendships, grow spiritually, and develop leadership skills that will serve them throughout their lives.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Weekly Youth Service (Sunday 2:00 PM)</li>
<li><i class="fas fa-check"></i> Youth Bible Study</li>
<li><i class="fas fa-check"></i> Leadership Training</li>
<li><i class="fas fa-check"></i> Summer Camps & Retreats</li>
<li><i class="fas fa-check"></i> Community Outreach</li>
</ul>''', 1),
                ('Children\'s Ministry', 'fas fa-child', '''<p>Our Children's Ministry provides a safe, fun, and biblically grounded environment for children to grow in their faith. We believe it's never too early to start a journey with Jesus.</p>
<p>Through creative learning, worship, and fellowship, we help children develop a strong foundation of faith that will guide them throughout their lives.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Sunday School</li>
<li><i class="fas fa-check"></i> Children's Church</li>
<li><i class="fas fa-check"></i> Vacation Bible School</li>
<li><i class="fas fa-check"></i> Children's Choir</li>
<li><i class="fas fa-check"></i> Youth Mentorship</li>
</ul>''', 2),
                ('Worship Ministry', 'fas fa-music', '''<p>Our Worship Ministry creates an atmosphere where people can encounter God's presence through praise and worship. We use music, song, and creative expression to glorify God and lead others into worship.</p>
<p>Whether you sing, play an instrument, or simply love to worship, there's a place for you on our worship team.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Main Worship Team</li>
<li><i class="fas fa-check"></i> Choir Ministry</li>
<li><i class="fas fa-check"></i> Instrumental Team</li>
<li><i class="fas fa-check"></i> Dance Ministry</li>
<li><i class="fas fa-check"></i> Sound & Media Team</li>
</ul>''', 3),
                ('Prayer Ministry', 'fas fa-pray', '''<p>Our Prayer Ministry exists to intercede for the church, community, and world. We believe in the power of prayer and its ability to bring about transformation and breakthrough.</p>
<p>Join us as we seek God's face and intercede for the needs of others.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Weekly Prayer Meeting (Friday 6:00 PM)</li>
<li><i class="fas fa-check"></i> Prayer Chain Network</li>
<li><i class="fas fa-check"></i> Morning Prayer Sessions</li>
<li><i class="fas fa-check"></i> Prayer Walks</li>
<li><i class="fas fa-check"></i> Intercessory Prayer Team</li>
</ul>''', 4),
                ('Community Outreach', 'fas fa-hands-helping', '''<p>Our Outreach Ministry is committed to meeting the physical and spiritual needs of our community. We believe in being the hands and feet of Jesus by serving those around us.</p>
<p>From health camps to food drives, we actively seek opportunities to demonstrate God's love in practical ways.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Health Camps</li>
<li><i class="fas fa-check"></i> Food Drives</li>
<li><i class="fas fa-check"></i> School Support Programs</li>
<li><i class="fas fa-check"></i> Evangelism & Discipleship</li>
<li><i class="fas fa-check"></i> Emergency Relief</li>
</ul>''', 5),
                ('Women\'s Ministry', 'fas fa-female', '''<p>Our Women's Ministry creates a space for women to grow in faith, build meaningful relationships, and discover their God-given purpose. We encourage women of all ages to connect and encourage one another.</p>
<p>Through fellowship, Bible study, and mentorship, we seek to empower women to live out their God-given potential.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Women's Fellowship</li>
<li><i class="fas fa-check"></i> Bible Study Groups</li>
<li><i class="fas fa-check"></i> Mentorship Program</li>
<li><i class="fas fa-check"></i> Women's Retreats</li>
<li><i class="fas fa-check"></i> Service Projects</li>
</ul>''', 6),
                ('Men\'s Ministry', 'fas fa-male', '''<p>Our Men's Ministry challenges men to grow in their faith, lead their families with integrity, and serve the church and community with excellence. We create spaces for honest fellowship and spiritual growth.</p>
<p>Through accountability groups, Bible study, and brotherhood, we seek to raise up godly men who lead with wisdom and grace.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Men's Fellowship</li>
<li><i class="fas fa-check"></i> Bible Study Groups</li>
<li><i class="fas fa-check"></i> Mentorship & Discipleship</li>
<li><i class="fas fa-check"></i> Men's Retreats</li>
<li><i class="fas fa-check"></i> Service Projects</li>
</ul>''', 7),
                ('Ushers & Hospitality', 'fas fa-concierge-bell', '''<p>Our Ushers & Hospitality Ministry ensures everyone who walks through our doors feels welcomed and cared for. We take pride in creating a warm, hospitable environment for all visitors and members.</p>
<p>Every person who enters our church should feel the love of Christ through our hospitality.</p>
<ul class="ministry-features">
<li><i class="fas fa-check"></i> Sunday Service Ushers</li>
<li><i class="fas fa-check"></i> Welcome Center</li>
<li><i class="fas fa-check"></i> New Visitor Follow-up</li>
<li><i class="fas fa-check"></i> Refreshments Team</li>
<li><i class="fas fa-check"></i> Parking Team</li>
</ul>''', 8),
            ]
            for name, icon, desc, order in ministries_data:
                Ministry.objects.create(name=name, icon=icon, description=desc, display_order=order, is_active=True)
            self.stdout.write(self.style.SUCCESS('✓ Ministries created'))
        else:
            self.stdout.write('✓ Ministries already exists')

        # Service Times
        if not ServiceTime.objects.exists():
            ServiceTime.objects.create(name='Sunday Service', day='Sunday', time='9:00 AM', description='Main worship service', is_active=True)
            ServiceTime.objects.create(name='Youth Service', day='Sunday', time='2:00 PM', description='Service for young people', is_active=True)
            ServiceTime.objects.create(name='Bible Study', day='Wednesday', time='7:00 PM', description='Mid-week Bible study', is_active=True)
            ServiceTime.objects.create(name='Prayer Meeting', day='Friday', time='6:00 PM', description='Weekly prayer meeting', is_active=True)
            ServiceTime.objects.create(name='Morning Prayer', day='Daily', time='6:00 AM', description='Daily morning prayer', is_active=True)
            self.stdout.write(self.style.SUCCESS('✓ Service Times created'))
        else:
            self.stdout.write('✓ Service Times already exists')

        # Events
        if not Event.objects.exists():
            base_date = timezone.now()
            events_data = [
                ('Church Anniversary', base_date + timedelta(days=180), 'Main Sanctuary', 'Celebrating another year of God\'s faithfulness! Join us for a special anniversary celebration with special music, testimonies, and a powerful message from God\'s Word.', 3),
                ('Youth Camp', base_date + timedelta(days=90), 'Camp Ground', 'An exciting camp experience for youth with worship, teaching, team building, and fun activities. A great opportunity for spiritual growth and friendship.', 2),
                ('New Year Prayer', base_date + timedelta(days=7), 'Main Sanctuary', 'Start the new year in prayer! Join us for an early morning prayer session to dedicate the year to God and seek His guidance.', 1),
                ('Christmas Carol Service', base_date - timedelta(days=60), 'Main Sanctuary', 'A special Christmas celebration featuring traditional and contemporary carols, dramatic presentations, and the true meaning of Christmas.', 3),
                ('Leadership Conference', base_date - timedelta(days=90), 'Main Sanctuary', 'Equipping and empowering church leaders with tools for effective ministry. Featuring guest speakers and practical workshops.', 2),
                ('Couples Fellowship', base_date - timedelta(days=100), 'Fellowship Hall', 'An evening for married couples to connect, learn, and strengthen their relationships through God\'s word.', 1),
                ('Thanksgiving Sunday', base_date - timedelta(days=107), 'Main Sanctuary', 'A special service to give thanks to God for His faithfulness and blessings. Bring your thanksgiving offerings and testimonies.', 3),
                ('Community Health Camp', base_date - timedelta(days=114), 'Church Grounds', 'Free health screenings, consultations, and health education for the Wamala community. Partnering with local health professionals.', 2),
                ('Youth Revival Service', base_date - timedelta(days=120), 'Main Sanctuary', 'A powerful evening of worship, prayer, and word as our youth come together to seek God\'s face and be refreshed in His presence.', 1),
            ]
            for title, start, loc, desc, days in events_data:
                Event.objects.create(
                    title=title,
                    start_date=start,
                    location=loc,
                    description=f'<p>{desc}</p>',
                    is_published=True,
                )
            self.stdout.write(self.style.SUCCESS('✓ Events created'))
        else:
            self.stdout.write('✓ Events already exists')

        # Sermons
        if not Sermon.objects.exists():
            sermons_data = [
                ('The Power of Faith', 'Pastor Milly Nankabirwa - Senior Pastor', '2024-10-15', 
                 '<p><strong>Series:</strong> Walking in Faith Series</p><p><strong>Scripture:</strong> Hebrews 11:1</p><p>Discover how faith can move mountains and transform your life as we explore the heroes of faith in Scripture.</p><p><strong>Duration:</strong> 45 min</p>',
                 True),
                ('Walking in God\'s Purpose', 'Pastor Milly Nankabirwa - Senior Pastor', '2024-10-08',
                 '<p><strong>Series:</strong> Discovering Your Destiny Series</p><p><strong>Scripture:</strong> Jeremiah 29:11</p><p>Learn how to discover and walk in the purpose God has for your life.</p><p><strong>Duration:</strong> 42 min</p>',
                 True),
                ('The Love of Christ', 'Youth Pastor - Youth Ministry Leader', '2024-10-01',
                 '<p><strong>Series:</strong> Deepening Your Love Series</p><p><strong>Scripture:</strong> John 3:16</p><p>Exploring the depth of God\'s love for us and how it transforms every aspect of our lives.</p><p><strong>Duration:</strong> 40 min</p>',
                 True),
                ('Overcoming Trials', 'Pastor Emmanuel - Worship Pastor', '2024-09-24',
                 '<p><strong>Series:</strong> Victory in Christ Series</p><p><strong>Scripture:</strong> Romans 8:37</p><p>Finding victory and strength through Christ in the midst of life\'s challenges.</p><p><strong>Duration:</strong> 38 min</p>',
                 True),
                ('Prayer That Moves Heaven', 'Pastor Milly Nankabirwa - Senior Pastor', '2024-09-17',
                 '<p><strong>Series:</strong> Power of Prayer Series</p><p><strong>Scripture:</strong> James 5:16</p><p>Discover the power of prayer and how to pray effectively for transformation.</p><p><strong>Duration:</strong> 50 min</p>',
                 True),
                ('Living as Disciples', 'Youth Pastor - Youth Ministry Leader', '2024-09-10',
                 '<p><strong>Series:</strong> Following Christ Series</p><p><strong>Scripture:</strong> Matthew 28:19-20</p><p>What it means to be a true disciple of Christ in today\'s world.</p><p><strong>Duration:</strong> 44 min</p>',
                 True),
            ]
            for title, speaker, date, desc, featured in sermons_data:
                Sermon.objects.create(
                    title=title,
                    speaker=speaker,
                    date_preached=date,
                    description=desc,
                    is_featured=featured,
                    is_published=True,
                )
            self.stdout.write(self.style.SUCCESS('✓ Sermons created'))
        else:
            self.stdout.write('✓ Sermons already exists')

        # Testimonials
        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                name='Grace Akello',
                testimony='I visited for the first time while passing through Wamala. The welcome was genuine, and I felt the presence of God in the service. This church has truly become my spiritual home.',
                is_approved=True,
                is_featured=True,
            )
            Testimonial.objects.create(
                name='David Okello',
                testimony='As a youth, I found a place where I belong. The youth ministry has helped me discover my purpose and grow closer to God. I\'m grateful for the leadership and community here.',
                is_approved=True,
                is_featured=True,
            )
            Testimonial.objects.create(
                name='Sarah Namuli',
                testimony='Laver Transformation Ministries changed my life. The community here feels like family, and I\'ve grown spiritually in ways I never imagined possible.',
                is_approved=True,
                is_featured=True,
            )
            self.stdout.write(self.style.SUCCESS('✓ Testimonials created'))
        else:
            self.stdout.write('✓ Testimonials already exists')

        # Giving Info
        if not GivingInfo.objects.exists():
            GivingInfo.objects.create(
                title='Support Our Ministry',
                description='Your generous giving helps us continue our mission to transform lives through God\'s Word. Thank you for your partnership in the Gospel!',
                mtn_mobile='MTN: XXXXXXXXXX',
                airtel_mobile='Airtel: XXXXXXXXXX',
            )
            self.stdout.write(self.style.SUCCESS('✓ Giving Info created'))
        else:
            self.stdout.write('✓ Giving Info already exists')

        self.stdout.write(self.style.SUCCESS('\n✓ All content seeded successfully!'))
