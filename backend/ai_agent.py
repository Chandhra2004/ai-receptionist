import openai
from typing import Optional, Dict, Any, List
from config import settings
from database_firebase import db  # Using Firebase Firestore
import json


# Salon business knowledge base (initial prompt context)
SALON_KNOWLEDGE = """
You are an AI receptionist for "Glamour Haven Salon", a premium beauty salon.

BUSINESS INFORMATION:
- Name: Glamour Haven Salon
- Location: 123 Beauty Street, Downtown
- Hours: Monday-Saturday 9 AM - 8 PM, Sunday 10 AM - 6 PM
- Phone: (555) 123-4567

SERVICES OFFERED:
1. Haircuts & Styling
   - Women's Cut: $65
   - Men's Cut: $45
   - Children's Cut: $30
   - Blow Dry & Style: $40

2. Hair Coloring
   - Full Color: $120
   - Highlights: $150
   - Balayage: $180

3. Treatments
   - Deep Conditioning: $50
   - Keratin Treatment: $250

4. Nails
   - Manicure: $35
   - Pedicure: $50
   - Gel Nails: $60

5. Spa Services
   - Facial: $85
   - Massage (60 min): $100

BOOKING POLICY:
- Appointments can be booked online or by phone
- 24-hour cancellation policy
- Late arrivals may result in shortened service time

STAFF:
- Sarah (Senior Stylist) - Specializes in color
- Mike (Master Barber) - Men's cuts and grooming
- Lisa (Nail Technician)
- Emma (Esthetician) - Facials and skincare

IMPORTANT INSTRUCTIONS:
- Be friendly, professional, and helpful
- If you don't know the answer to a question, say: "Let me check with my supervisor and get back to you."
- Never make up information
- Always confirm appointment details
"""


class AIAgent:
    """AI Agent for handling customer calls and questions."""
    
    def __init__(self):
        """Initialize the AI agent."""
        openai.api_key = settings.openai_api_key
        self.system_prompt = SALON_KNOWLEDGE
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
    
    async def process_question(
        self,
        question: str,
        customer_id: str,
        customer_phone: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a customer question and determine if escalation is needed.
        
        Returns:
            Dict with response, needs_help flag, and optional help_request_id
        """
        # Initialize conversation history for new customer
        if customer_id not in self.conversation_history:
            self.conversation_history[customer_id] = []
        
        # First, check if we have learned knowledge about this question
        knowledge_results = await db.search_knowledge(question)
        
        if knowledge_results:
            # Use the most relevant learned knowledge
            learned_answer = knowledge_results[0]['answer']
            await db.increment_knowledge_usage(knowledge_results[0]['id'])
            
            return {
                'response': learned_answer,
                'needs_help': False,
                'help_request_id': None,
                'knowledge_used': knowledge_results[0]['id']
            }
        
        # Build conversation context
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": """
            ESCALATION RULES:
            - If the question is about something not covered in your knowledge base, respond with: "Let me check with my supervisor and get back to you."
            - If the customer asks about specific availability, pricing not listed, or special requests, escalate.
            - If you're uncertain about any information, escalate rather than guessing.
            - When escalating, be polite and assure the customer you'll get back to them soon.
            
            To escalate, include [ESCALATE] at the start of your response.
            """}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[customer_id][-5:])  # Last 5 exchanges
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Check if escalation is needed
            needs_escalation = ai_response.startswith("[ESCALATE]")
            
            if needs_escalation:
                # Remove the [ESCALATE] tag
                ai_response = ai_response.replace("[ESCALATE]", "").strip()
                
                # Create help request
                help_request_id = await db.create_help_request(
                    question=question,
                    customer_id=customer_id,
                    customer_phone=customer_phone,
                    context={
                        'conversation_history': self.conversation_history[customer_id][-3:],
                        'additional_context': context or {}
                    }
                )
                
                # Use a friendly escalation message
                escalation_message = "Let me check with my supervisor and get back to you shortly. We'll call you back with the answer!"
                
                # Update conversation history
                self.conversation_history[customer_id].append({"role": "user", "content": question})
                self.conversation_history[customer_id].append({"role": "assistant", "content": escalation_message})
                
                return {
                    'response': escalation_message,
                    'needs_help': True,
                    'help_request_id': help_request_id,
                    'knowledge_used': None
                }
            else:
                # Update conversation history
                self.conversation_history[customer_id].append({"role": "user", "content": question})
                self.conversation_history[customer_id].append({"role": "assistant", "content": ai_response})
                
                return {
                    'response': ai_response,
                    'needs_help': False,
                    'help_request_id': None,
                    'knowledge_used': None
                }
        
        except Exception as e:
            print(f"Error processing question with OpenAI: {e}")
            # Fallback to escalation on error
            help_request_id = await db.create_help_request(
                question=question,
                customer_id=customer_id,
                customer_phone=customer_phone,
                context={'error': str(e)}
            )
            
            return {
                'response': "I'm having trouble processing your request. Let me get a supervisor to help you.",
                'needs_help': True,
                'help_request_id': help_request_id,
                'knowledge_used': None
            }
    
    async def handle_supervisor_response(
        self,
        request_id: str,
        supervisor_answer: str,
        supervisor_id: str
    ) -> bool:
        """
        Handle supervisor's response to a help request.
        
        This will:
        1. Update the help request
        2. Add to knowledge base
        3. Simulate follow-up with customer
        """
        # Get the original request
        request = await db.get_help_request(request_id)
        if not request:
            print(f"Request {request_id} not found")
            return False
        
        # Update the help request
        await db.update_help_request(
            request_id=request_id,
            supervisor_answer=supervisor_answer,
            supervisor_id=supervisor_id,
            status='resolved'
        )
        
        # Add to knowledge base
        await db.add_knowledge(
            question=request['question'],
            answer=supervisor_answer,
            source='supervisor',
            tags=['learned', 'supervisor_response']
        )
        
        # Simulate follow-up with customer
        await self.follow_up_with_customer(
            customer_id=request['customer_id'],
            customer_phone=request.get('customer_phone'),
            question=request['question'],
            answer=supervisor_answer
        )
        
        print(f"✅ Supervisor response processed for request {request_id}")
        return True
    
    async def follow_up_with_customer(
        self,
        customer_id: str,
        customer_phone: Optional[str],
        question: str,
        answer: str
    ):
        """
        Simulate following up with the customer.
        In production, this would send an SMS or make a call.
        """
        print("\n" + "="*60)
        print("📞 SIMULATED CUSTOMER FOLLOW-UP")
        print("="*60)
        print(f"To: Customer {customer_id}")
        if customer_phone:
            print(f"Phone: {customer_phone}")
        print(f"\nOriginal Question: {question}")
        print(f"\nAI Response: Hi! I checked with my supervisor about your question. {answer}")
        print("="*60 + "\n")
        
        # Update conversation history
        if customer_id in self.conversation_history:
            self.conversation_history[customer_id].append({
                "role": "assistant",
                "content": f"Following up on your question: {question}. Here's the answer: {answer}"
            })
    
    def clear_conversation_history(self, customer_id: str):
        """Clear conversation history for a customer."""
        if customer_id in self.conversation_history:
            del self.conversation_history[customer_id]


# Global AI agent instance
agent = AIAgent()
