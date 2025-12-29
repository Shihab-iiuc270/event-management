# import os
# import django
# import random
# from faker import Faker
# from datetime import timedelta
# from django.utils import timezone

# # ---------------- SETUP DJANGO ----------------
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
# django.setup()

# from events.models import Category, Event, Participant


# def populate_db():
#     fake = Faker()
#     print("🚀 Starting database population...")

#     # ---------------- CATEGORIES ----------------
#     print("\n📁 Creating categories...")
#     categories_data = [
#         ("Sports", "Sports events and competitions"),
#         ("Business", "Business meetings and conferences"),
#         ("Education", "Educational workshops and seminars"),
#         ("Music", "Concerts and music shows"),
#         ("Technology", "Tech events and hackathons"),
#         ("Health", "Health and wellness programs"),
#         ("Social", "Social and community events"),
#         ("Charity", "Fundraising and charity events"),
#     ]

#     categories = []
#     for name, desc in categories_data:
#         category, _ = Category.objects.get_or_create(
#             name=name,
#             defaults={"description": desc}
#         )
#         categories.append(category)

#     print(f"✅ Categories ready: {len(categories)}")

#     # ---------------- PARTICIPANTS ----------------
#     print("\n👥 Creating participants...")
#     participants = []

#     for i in range(15):
#         participant = Participant.objects.create(
#             name=fake.name(),
#             email=f"participant{i+1}@example.com"
#         )
#         participants.append(participant)

#     print(f"✅ Participants created: {len(participants)}")

#     # ---------------- EVENTS ----------------
#     print("\n📅 Creating events...")
#     events = []

#     for i in range(20):
#         category = random.choice(categories)

#         event = Event.objects.create(
#             name=fake.catch_phrase(),
#             description=fake.paragraph(nb_sentences=3),
#             date=timezone.now().date() + timedelta(days=random.randint(1, 30)),
#             time=fake.time_object(),
#             location=fake.city(),
#             category=category
#         )

#         # ✅ ManyToMany (CORRECT WAY)
#         selected_participants = random.sample(participants, random.randint(2, 5))
#         event.participants.set(selected_participants)

#         events.append(event)
#         print(f"  ✓ {event.name} ({category.name})")

#     # ---------------- SUMMARY ----------------
#     print("\n" + "=" * 50)
#     print("📊 DATABASE POPULATION SUMMARY")
#     print("=" * 50)

#     print(f"🏷️ Categories: {Category.objects.count()}")
#     print(f"📅 Events: {Event.objects.count()}")
#     print(f"👥 Participants: {Participant.objects.count()}")

#     print("\n🎉 Database populated successfully!")


# if __name__ == "__main__":
#     populate_db()
