"""
Firebase Firestore database implementation.
Production-ready with real cloud database.
"""

import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Optional, List, Dict, Any
from config import settings
import os


class FirebaseDatabase:
    """Firebase Firestore database - production ready!"""
    
    def __init__(self):
        """Initialize Firebase connection."""
        if not firebase_admin._apps:
            if os.path.exists(settings.firebase_credentials_path):
                print(f"🔥 Initializing Firebase from {settings.firebase_credentials_path}")
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized successfully")
            else:
                print(f"⚠️  Firebase credentials not found at {settings.firebase_credentials_path}")
                print("⚠️  Using application default credentials")
                firebase_admin.initialize_app()
        
        self.db = firestore.client()
        self.requests_collection = self.db.collection('help_requests')
        self.knowledge_collection = self.db.collection('knowledge_base')
        
        # Add sample knowledge if database is empty
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Add sample knowledge if database is empty."""
        try:
            # Check if knowledge base is empty
            docs = list(self.knowledge_collection.limit(1).stream())
            if not docs:
                print("📚 Initializing sample knowledge base...")
                self._add_sample_knowledge()
                print("✅ Sample knowledge added")
        except Exception as e:
            print(f"⚠️  Error checking/adding sample data: {e}")
    
    def _add_sample_knowledge(self):
        """Add sample knowledge for testing."""
        sample_knowledge = [
            {
                "question": "What are your hours?",
                "answer": "We're open Monday-Saturday 9 AM - 8 PM, and Sunday 10 AM - 6 PM.",
                "tags": ["hours", "schedule"],
                "source": "initial"
            },
            {
                "question": "How much is a haircut?",
                "answer": "Men's haircut is $25, women's haircut starts at $45.",
                "tags": ["pricing", "haircut"],
                "source": "initial"
            },
            {
                "question": "Do you take walk-ins?",
                "answer": "Yes! We accept walk-ins, but appointments are recommended to avoid wait times.",
                "tags": ["appointments", "walk-ins"],
                "source": "initial"
            },
            {
                "question": "Where are you located?",
                "answer": "We're located at 123 Main Street, Downtown. Free parking available in the rear.",
                "tags": ["location", "parking"],
                "source": "initial"
            }
        ]
        
        for kb in sample_knowledge:
            doc_ref = self.knowledge_collection.document()
            kb['id'] = doc_ref.id
            kb['created_at'] = firestore.SERVER_TIMESTAMP
            kb['updated_at'] = firestore.SERVER_TIMESTAMP
            kb['usage_count'] = 0
            doc_ref.set(kb)
    
    # Help Requests Management
    
    async def create_help_request(
        self,
        question: str,
        customer_id: str,
        customer_phone: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a new help request."""
        doc_ref = self.requests_collection.document()
        request_data = {
            'id': doc_ref.id,
            'question': question,
            'customer_id': customer_id,
            'customer_phone': customer_phone,
            'context': context or {},
            'status': 'pending',
            'created_at': firestore.SERVER_TIMESTAMP,
            'resolved_at': None,
            'supervisor_answer': None,
            'supervisor_id': None
        }
        doc_ref.set(request_data)
        print(f"📝 Created help request: {doc_ref.id}")
        return doc_ref.id
    
    async def get_help_request(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific help request by ID."""
        doc = self.requests_collection.document(request_id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    
    async def get_pending_requests(self) -> List[Dict[str, Any]]:
        """Get all pending help requests."""
        try:
            docs = self.requests_collection.where(
                'status', '==', 'pending'
            ).order_by(
                'created_at', direction=firestore.Query.DESCENDING
            ).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"⚠️  Error getting pending requests: {e}")
            return []
    
    async def get_all_requests(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all help requests with optional limit."""
        try:
            docs = self.requests_collection.order_by(
                'created_at', direction=firestore.Query.DESCENDING
            ).limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"⚠️  Error getting all requests: {e}")
            return []
    
    async def update_help_request(
        self,
        request_id: str,
        supervisor_answer: str,
        supervisor_id: str,
        status: str = 'resolved'
    ) -> bool:
        """Update a help request with supervisor's answer."""
        try:
            self.requests_collection.document(request_id).update({
                'supervisor_answer': supervisor_answer,
                'supervisor_id': supervisor_id,
                'status': status,
                'resolved_at': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Updated request {request_id} to {status}")
            return True
        except Exception as e:
            print(f"❌ Error updating help request: {e}")
            return False
    
    async def mark_request_unresolved(self, request_id: str) -> bool:
        """Mark a request as unresolved (timeout)."""
        try:
            self.requests_collection.document(request_id).update({
                'status': 'unresolved',
                'resolved_at': firestore.SERVER_TIMESTAMP
            })
            print(f"⚠️  Marked request {request_id} as unresolved")
            return True
        except Exception as e:
            print(f"❌ Error marking request as unresolved: {e}")
            return False
    
    # Knowledge Base Management
    
    async def add_knowledge(
        self,
        question: str,
        answer: str,
        source: str = 'supervisor',
        tags: Optional[List[str]] = None
    ) -> str:
        """Add new knowledge to the knowledge base."""
        doc_ref = self.knowledge_collection.document()
        knowledge_data = {
            'id': doc_ref.id,
            'question': question,
            'answer': answer,
            'source': source,
            'tags': tags or [],
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'usage_count': 0
        }
        doc_ref.set(knowledge_data)
        print(f"📚 Added knowledge: {question[:50]}...")
        return doc_ref.id
    
    async def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant answers."""
        try:
            # Get all knowledge entries (Firestore doesn't support full-text search natively)
            docs = self.knowledge_collection.stream()
            results = []
            query_lower = query.lower()
            
            for doc in docs:
                data = doc.to_dict()
                if query_lower in data['question'].lower() or query_lower in data['answer'].lower():
                    results.append(data)
            
            return results
        except Exception as e:
            print(f"⚠️  Error searching knowledge: {e}")
            return []
    
    async def get_all_knowledge(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all knowledge base entries."""
        try:
            docs = self.knowledge_collection.order_by(
                'created_at', direction=firestore.Query.DESCENDING
            ).limit(limit).stream()
            return [doc.to_dict() for doc in docs]
        except Exception as e:
            print(f"⚠️  Error getting knowledge: {e}")
            return []
    
    async def update_knowledge(self, knowledge_id: str, answer: str) -> bool:
        """Update an existing knowledge base entry."""
        try:
            self.knowledge_collection.document(knowledge_id).update({
                'answer': answer,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Updated knowledge: {knowledge_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating knowledge: {e}")
            return False
    
    async def increment_knowledge_usage(self, knowledge_id: str) -> bool:
        """Increment usage count for a knowledge entry."""
        try:
            self.knowledge_collection.document(knowledge_id).update({
                'usage_count': firestore.Increment(1)
            })
            return True
        except Exception as e:
            print(f"❌ Error incrementing knowledge usage: {e}")
            return False


# Global database instance
db = FirebaseDatabase()
