// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';

// API Endpoints
export const API_ENDPOINTS = {
  // Requests
  PENDING_REQUESTS: `${API_BASE_URL}/api/requests/pending`,
  ALL_REQUESTS: `${API_BASE_URL}/api/requests/all`,
  RESPOND_REQUEST: `${API_BASE_URL}/api/requests/respond`,
  GET_REQUEST: (id) => `${API_BASE_URL}/api/requests/${id}`,
  
  // Knowledge Base
  ALL_KNOWLEDGE: `${API_BASE_URL}/api/knowledge/all`,
  ADD_KNOWLEDGE: `${API_BASE_URL}/api/knowledge/add`,
  SEARCH_KNOWLEDGE: `${API_BASE_URL}/api/knowledge/search`,
  
  // Calls
  SIMULATE_CALL: `${API_BASE_URL}/api/calls/simulate`,
  ACTIVE_CALLS: `${API_BASE_URL}/api/calls/active`,
  CALL_LOGS: `${API_BASE_URL}/api/calls/logs`,
  
  // Stats
  STATS: `${API_BASE_URL}/api/stats`,
};
