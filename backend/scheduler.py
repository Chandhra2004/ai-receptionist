"""
Background scheduler to mark old pending requests as unresolved.
This runs periodically to check for requests that have been pending too long.
"""

import asyncio
from datetime import datetime, timedelta
from database_firebase import db


class RequestScheduler:
    """Check for old pending requests and mark them as unresolved."""
    
    def __init__(self, timeout_days: int = 2):
        """
        Initialize scheduler.
        
        Args:
            timeout_days: Number of days before marking request as unresolved
        """
        self.timeout_days = timeout_days
        self.is_running = False
    
    async def check_old_requests(self):
        """Check for requests older than timeout_days and mark as unresolved."""
        try:
            # Get all pending requests
            pending_requests = await db.get_pending_requests()
            
            now = datetime.now()
            timeout_threshold = now - timedelta(days=self.timeout_days)
            
            for request in pending_requests:
                # Parse created_at timestamp
                created_at = datetime.fromisoformat(request['created_at'])
                
                # Check if request is older than threshold
                if created_at < timeout_threshold:
                    print(f"⚠️  Marking request {request['id']} as unresolved (pending for {self.timeout_days}+ days)")
                    await db.mark_request_unresolved(request['id'])
        
        except Exception as e:
            print(f"Error checking old requests: {e}")
    
    async def start(self, check_interval_hours: int = 6):
        """
        Start the scheduler to check periodically.
        
        Args:
            check_interval_hours: How often to check (default: every 6 hours)
        """
        self.is_running = True
        print(f"🕐 Scheduler started: Checking every {check_interval_hours} hours for requests older than {self.timeout_days} days")
        
        while self.is_running:
            await self.check_old_requests()
            # Wait before next check
            await asyncio.sleep(check_interval_hours * 3600)
    
    def stop(self):
        """Stop the scheduler."""
        self.is_running = False
        print("🛑 Scheduler stopped")


# Global scheduler instance
scheduler = RequestScheduler(timeout_days=2)


# Usage in main.py:
"""
from scheduler import scheduler

@app.on_event("startup")
async def startup_event():
    # Start scheduler in background
    asyncio.create_task(scheduler.start(check_interval_hours=6))

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.stop()
"""
