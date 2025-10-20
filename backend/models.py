from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class RequestStatus(str, Enum):
    """Help request status enum."""
    PENDING = "pending"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"


class HelpRequest(BaseModel):
    """Help request model."""
    id: Optional[str] = None
    question: str
    customer_id: str
    customer_phone: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    status: RequestStatus = RequestStatus.PENDING
    created_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    supervisor_answer: Optional[str] = None
    supervisor_id: Optional[str] = None


class HelpRequestCreate(BaseModel):
    """Create help request payload."""
    question: str
    customer_id: str
    customer_phone: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class HelpRequestResponse(BaseModel):
    """Supervisor response to help request."""
    request_id: str
    supervisor_answer: str
    supervisor_id: str = "supervisor_1"


class KnowledgeBase(BaseModel):
    """Knowledge base entry model."""
    id: Optional[str] = None
    question: str
    answer: str
    source: str = "supervisor"
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    usage_count: int = 0


class KnowledgeCreate(BaseModel):
    """Create knowledge base entry payload."""
    question: str
    answer: str
    source: str = "supervisor"
    tags: Optional[List[str]] = None


class CallSimulation(BaseModel):
    """Simulated call payload."""
    customer_id: str
    customer_phone: str
    question: str
    customer_name: Optional[str] = "Customer"


class AgentResponse(BaseModel):
    """AI agent response model."""
    response: str
    needs_help: bool
    help_request_id: Optional[str] = None
    knowledge_used: Optional[str] = None
