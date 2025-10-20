from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import asyncio

from config import settings
from models import (
    HelpRequestCreate,
    HelpRequestResponse,
    KnowledgeCreate,
    CallSimulation,
    AgentResponse
)
from database_firebase import db  # Using Firebase Firestore for production
from ai_agent import agent
from livekit_handler import livekit_handler
from scheduler import scheduler  # Auto-mark old requests as unresolved

# Initialize FastAPI app
app = FastAPI(
    title="Frontdesk AI Receptionist API",
    description="Human-in-the-loop AI receptionist system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# WebSocket connections for real-time updates
class ConnectionManager:
    """Manage WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup."""
    print("🚀 Starting AI Receptionist API...")
    # Start scheduler to check for old pending requests
    asyncio.create_task(scheduler.start(check_interval_hours=6))
    print("✅ Scheduler started: Will check for requests older than 2 days every 6 hours")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop background tasks on server shutdown."""
    print("🛑 Shutting down AI Receptionist API...")
    scheduler.stop()


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Frontdesk AI Receptionist",
        "version": "1.0.0"
    }


# Call Simulation Endpoints

@app.post("/api/calls/simulate", response_model=AgentResponse)
async def simulate_call(call_data: CallSimulation):
    """
    Simulate an incoming call and process the customer's question.
    
    This endpoint:
    1. Simulates an incoming call via LiveKit
    2. Processes the customer's question through the AI agent
    3. Returns the response and escalation status
    """
    try:
        # Simulate incoming call
        call_id = await livekit_handler.simulate_incoming_call(
            customer_id=call_data.customer_id,
            customer_phone=call_data.customer_phone,
            customer_name=call_data.customer_name
        )
        
        # Process speech
        await livekit_handler.process_speech(call_id, call_data.question)
        
        # Get AI agent response
        result = await agent.process_question(
            question=call_data.question,
            customer_id=call_data.customer_id,
            customer_phone=call_data.customer_phone,
            context={'call_id': call_id}
        )
        
        # Send response via LiveKit
        await livekit_handler.send_speech_response(call_id, result['response'])
        
        # End call
        await livekit_handler.end_call(call_id)
        
        # Notify supervisor UI if escalation occurred
        if result['needs_help']:
            await manager.broadcast({
                'type': 'new_help_request',
                'request_id': result['help_request_id'],
                'question': call_data.question,
                'customer_id': call_data.customer_id
            })
        
        return AgentResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calls/active")
async def get_active_calls():
    """Get list of currently active calls."""
    return {
        "active_calls": livekit_handler.get_active_calls()
    }


@app.get("/api/calls/logs")
async def get_call_logs(limit: int = 50):
    """Get recent call logs."""
    return {
        "call_logs": livekit_handler.get_call_logs(limit)
    }


# Help Request Endpoints

@app.post("/api/requests/create")
async def create_help_request(request: HelpRequestCreate):
    """Create a new help request manually."""
    try:
        request_id = await db.create_help_request(
            question=request.question,
            customer_id=request.customer_id,
            customer_phone=request.customer_phone,
            context=request.context
        )
        
        # Notify supervisor UI
        await manager.broadcast({
            'type': 'new_help_request',
            'request_id': request_id,
            'question': request.question,
            'customer_id': request.customer_id
        })
        
        return {"request_id": request_id, "status": "created"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/requests/pending")
async def get_pending_requests():
    """Get all pending help requests."""
    try:
        requests = await db.get_pending_requests()
        return {"requests": requests, "count": len(requests)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/requests/all")
async def get_all_requests(limit: int = 100):
    """Get all help requests."""
    try:
        requests = await db.get_all_requests(limit)
        return {"requests": requests, "count": len(requests)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/requests/{request_id}")
async def get_help_request(request_id: str):
    """Get a specific help request."""
    try:
        request = await db.get_help_request(request_id)
        if not request:
            raise HTTPException(status_code=404, detail="Request not found")
        return request
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/requests/respond")
async def respond_to_request(response: HelpRequestResponse):
    """
    Supervisor responds to a help request.
    
    This will:
    1. Update the help request with the supervisor's answer
    2. Add the answer to the knowledge base
    3. Trigger a follow-up with the customer
    """
    try:
        success = await agent.handle_supervisor_response(
            request_id=response.request_id,
            supervisor_answer=response.supervisor_answer,
            supervisor_id=response.supervisor_id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Notify supervisor UI
        await manager.broadcast({
            'type': 'request_resolved',
            'request_id': response.request_id
        })
        
        return {
            "status": "success",
            "message": "Response processed and customer notified"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Knowledge Base Endpoints

@app.get("/api/knowledge/all")
async def get_all_knowledge(limit: int = 100):
    """Get all knowledge base entries."""
    try:
        knowledge = await db.get_all_knowledge(limit)
        return {"knowledge": knowledge, "count": len(knowledge)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/knowledge/add")
async def add_knowledge(knowledge: KnowledgeCreate):
    """Add a new knowledge base entry manually."""
    try:
        knowledge_id = await db.add_knowledge(
            question=knowledge.question,
            answer=knowledge.answer,
            source=knowledge.source,
            tags=knowledge.tags
        )
        return {"knowledge_id": knowledge_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge/search")
async def search_knowledge(query: str):
    """Search the knowledge base."""
    try:
        results = await db.search_knowledge(query)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates to supervisor UI."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
            # Echo back for heartbeat
            await websocket.send_json({"type": "heartbeat", "status": "ok"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Statistics endpoint
@app.get("/api/stats")
async def get_statistics():
    """Get system statistics."""
    try:
        all_requests = await db.get_all_requests(1000)
        all_knowledge = await db.get_all_knowledge(1000)
        
        pending_count = len([r for r in all_requests if r.get('status') == 'pending'])
        resolved_count = len([r for r in all_requests if r.get('status') == 'resolved'])
        unresolved_count = len([r for r in all_requests if r.get('status') == 'unresolved'])
        
        return {
            "total_requests": len(all_requests),
            "pending_requests": pending_count,
            "resolved_requests": resolved_count,
            "unresolved_requests": unresolved_count,
            "knowledge_base_size": len(all_knowledge),
            "active_calls": len(livekit_handler.get_active_calls())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
