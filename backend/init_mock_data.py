"""
Initialize mock data for demo purposes.
Run this script to populate the database with sample data.
"""

import asyncio
from database import db
from datetime import datetime


async def init_mock_data():
    """Initialize the database with mock data for demonstration."""
    
    print("🚀 Initializing mock data...")
    
    # Add initial knowledge base entries
    knowledge_entries = [
        {
            "question": "What are your business hours?",
            "answer": "We're open Monday-Saturday 9 AM - 8 PM, and Sunday 10 AM - 6 PM.",
            "tags": ["hours", "schedule", "timing"]
        },
        {
            "question": "How much does a women's haircut cost?",
            "answer": "A women's haircut costs $65.",
            "tags": ["pricing", "haircut", "women"]
        },
        {
            "question": "How much does a men's haircut cost?",
            "answer": "A men's haircut costs $45.",
            "tags": ["pricing", "haircut", "men"]
        },
        {
            "question": "What is your cancellation policy?",
            "answer": "We have a 24-hour cancellation policy. Please call us at least 24 hours in advance to cancel or reschedule your appointment.",
            "tags": ["policy", "cancellation", "appointments"]
        },
        {
            "question": "Do you offer hair coloring services?",
            "answer": "Yes! We offer full color for $120, highlights for $150, and balayage for $180.",
            "tags": ["services", "coloring", "pricing"]
        },
        {
            "question": "Where are you located?",
            "answer": "We're located at 123 Beauty Street, Downtown. You can find us easily with GPS.",
            "tags": ["location", "address", "directions"]
        },
        {
            "question": "What's your phone number?",
            "answer": "You can reach us at (555) 123-4567.",
            "tags": ["contact", "phone"]
        },
        {
            "question": "Do you offer manicure and pedicure services?",
            "answer": "Yes! Manicure is $35, pedicure is $50, and gel nails are $60.",
            "tags": ["services", "nails", "pricing"]
        },
    ]
    
    print("\n📚 Adding knowledge base entries...")
    for entry in knowledge_entries:
        knowledge_id = await db.add_knowledge(
            question=entry["question"],
            answer=entry["answer"],
            source="initial_setup",
            tags=entry["tags"]
        )
        print(f"  ✓ Added: {entry['question'][:50]}...")
    
    # Add some sample help requests (for demonstration)
    sample_requests = [
        {
            "question": "Do you have any special packages for weddings?",
            "customer_id": "CUST001",
            "customer_phone": "(555) 111-2222"
        },
        {
            "question": "Can I bring my pet to the salon?",
            "customer_id": "CUST002",
            "customer_phone": "(555) 333-4444"
        },
    ]
    
    print("\n🔔 Adding sample help requests...")
    for req in sample_requests:
        request_id = await db.create_help_request(
            question=req["question"],
            customer_id=req["customer_id"],
            customer_phone=req["customer_phone"]
        )
        print(f"  ✓ Created request: {req['question'][:50]}...")
    
    print("\n✅ Mock data initialization complete!")
    print("\nYou can now:")
    print("  1. Start the backend server: python main.py")
    print("  2. Start the frontend: cd ../frontend && npm start")
    print("  3. Visit http://localhost:3000 to see the supervisor UI")
    print("  4. Use the Call Simulator to test the AI receptionist")


if __name__ == "__main__":
    asyncio.run(init_mock_data())
