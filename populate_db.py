# import os
# import django
# from faker import Faker
# import random
# from datetime import datetime, timedelta
# from django.utils import timezone

# # Set up Django FIRST
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
# django.setup()

# # Import models AFTER django.setup()
# from events.models import Event, Participant, Category

# def populate_db():
#     fake = Faker()
    
#     print("🎯 Starting database population...")
    
#     # Check if migrations are applied
#     try:
#         # Test database connection
#         Category.objects.exists()
#         print("✅ Database connection successful")
#     except Exception as e:
#         print(f"❌ Database error: {e}")
#         print("💡 Please run: python manage.py migrate")
#         return
    
#     # 1. Create Categories with proper relationships
#     print("\n📁 Creating categories...")
#     categories_data = [
#         {"name": "Sports", "description": "Sports events, tournaments, and athletic competitions"},
#         {"name": "Business", "description": "Business meetings, conferences, and networking events"},
#         {"name": "Education", "description": "Educational workshops, seminars, and training sessions"},
#         {"name": "Music", "description": "Concerts, live performances, and music festivals"},
#         {"name": "Technology", "description": "Tech conferences, hackathons, and IT workshops"},
#         {"name": "Health", "description": "Health awareness programs and wellness workshops"},
#         {"name": "Social", "description": "Social gatherings, parties, and community events"},
#         {"name": "Charity", "description": "Fundraising events and volunteer activities"}
#     ]
    
#     categories = []
#     for data in categories_data:
#         # Use get_or_create to avoid duplicates
#         category, created = Category.objects.get_or_create(
#             name=data["name"],
#             defaults={"description": data["description"]}
#         )
#         categories.append(category)
#         if created:
#             print(f"  ✓ Created category: {data['name']}")
#         else:
#             print(f"  ⚡ Using existing category: {data['name']}")
    
#     print(f"✅ Total categories: {len(categories)}")
    
#     # 2. Create Participants with proper relationships
#     print("\n👥 Creating participants...")
#     participants = []
    
#     for i in range(15):
#         # Create unique email
#         base_email = f"participant{i+1}@example.com"
#         email = base_email
        
#         # Check if email exists
#         counter = 1
#         while Participant.objects.filter(email=email).exists():
#             email = f"participant{i+1}_{counter}@example.com"
#             counter += 1
        
#         participant = Participant.objects.create(
#             name=fake.name(),
#             email=email
#         )
#         participants.append(participant)
#         print(f"  ✓ Created participant: {participant.name}")
    
#     print(f"✅ Total participants: {len(participants)}")
    
#     # 3. Create Events with proper relationships
#     print("\n📅 Creating events...")
    
#     # Event names by category
#     event_templates = {
#         "Sports": [
#             "Annual Sports Day", "Football Tournament", "Cricket Championship",
#             "Marathon 2024", "Swimming Competition", "Basketball League"
#         ],
#         "Business": [
#             "Business Conference", "Networking Meetup", "Startup Pitch",
#             "Corporate Training", "Leadership Summit", "Annual Meeting"
#         ],
#         "Education": [
#             "Programming Workshop", "Science Seminar", "Career Counseling",
#             "Language Class", "Exam Preparation", "Skill Development"
#         ],
#         "Music": [
#             "Live Concert", "Music Festival", "DJ Night",
#             "Classical Music Evening", "Rock Show", "Jazz Performance"
#         ],
#         "Technology": [
#             "Tech Conference", "Hackathon", "AI Workshop",
#             "Cybersecurity Seminar", "Web Development Bootcamp", "IoT Meetup"
#         ]
#     }
    
#     events = []
#     for i in range(20):
#         # Pick random category
#         category = random.choice(categories)
        
#         # Get event name
#         if category.name in event_templates:
#             event_name = random.choice(event_templates[category.name])
#         else:
#             event_name = f"{category.name} Event {i+1}"
        
#         # Generate future dates (next 30 days)
#         event_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
        
#         # Generate time
#         hour = random.randint(9, 20)
#         minute = random.choice([0, 15, 30, 45])
        
#         event = Event.objects.create(
#             name=event_name,
#             description=fake.paragraph(nb_sentences=3),
#             date=event_date,
#             time=datetime.strptime(f"{hour:02d}:{minute:02d}", "%H:%M").time(),
#             location=fake.city(),
#             category=category
#         )
        
#         # Assign participants (2-4 per event)
#         num_participants = random.randint(2, min(4, len(participants)))
#         selected_participants = random.sample(participants, num_participants)
#         event.assign_to.set(selected_participants)
        
#         events.append(event)
#         print(f"  ✓ Created event: {event_name} ({category.name})")
    
#     print(f"✅ Total events created: {len(events)}")
    
#     # 4. Show summary
#     print("\n" + "="*60)
#     print("📊 DATABASE POPULATION SUMMARY")
#     print("="*60)
    
#     print(f"\n🏷️  Categories: {Category.objects.count()}")
#     for cat in Category.objects.all():
#         event_count = Event.objects.filter(category=cat).count()
#         print(f"   • {cat.name}: {event_count} events")
    
#     print(f"\n👥 Participants: {Participant.objects.count()}")
#     print(f"📅 Total Events: {Event.objects.count()}")
    
#     # Show sample events
#     print("\n🎯 Sample Events Created:")
#     print("-"*40)
#     sample_events = Event.objects.all()[:3]
#     for event in sample_events:
#         participants_names = ", ".join([p.name for p in event.assign_to.all()[:2]])
#         date_str = event.date.strftime("%b %d, %Y")
#         time_str = event.time.strftime("%I:%M %p")
#         print(f"• {event.name}")
#         print(f"  📅 {date_str} | 🕒 {time_str} | 🏷️ {event.category.name}")
#         print(f"  👥 Participants: {participants_names}")
#         if event.assign_to.count() > 2:
#             print(f"    + {event.assign_to.count() - 2} more participants")
#         print()
    
#     print("🎉 Database populated successfully!")
#     print("💡 You can now access the data in Django admin or your views.")

# if __name__ == "__main__":
#     populate_db()