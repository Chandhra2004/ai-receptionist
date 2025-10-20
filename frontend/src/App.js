import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PendingRequests from './components/PendingRequests';
import RequestHistory from './components/RequestHistory';
import KnowledgeBase from './components/KnowledgeBase';
import CallSimulator from './components/CallSimulator';
import { WS_URL } from './config';

function Navigation() {
  const location = useLocation();
  
  const navItems = [
    { name: 'Dashboard', path: '/', icon: '📊' },
    { name: 'Pending Requests', path: '/pending', icon: '🔔' },
    { name: 'Request History', path: '/history', icon: '📜' },
    { name: 'Knowledge Base', path: '/knowledge', icon: '📚' },
    { name: 'Call Simulator', path: '/simulator', icon: '📞' },
  ];
  
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <div className="flex-shrink-0 flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">
                🤖 Frontdesk AI
              </h1>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    location.pathname === item.path
                      ? 'border-primary-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  const [wsConnected, setWsConnected] = useState(false);
  const [notifications, setNotifications] = useState([]);
  
  useEffect(() => {
    // WebSocket connection for real-time updates
    const ws = new WebSocket(WS_URL);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setWsConnected(true);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log('WebSocket message:', data);
      
      if (data.type === 'new_help_request') {
        setNotifications(prev => [...prev, {
          id: Date.now(),
          type: 'new_request',
          message: `New help request: ${data.question}`,
          timestamp: new Date()
        }]);
        
        // Play notification sound (optional)
        // new Audio('/notification.mp3').play();
      } else if (data.type === 'request_resolved') {
        setNotifications(prev => [...prev, {
          id: Date.now(),
          type: 'resolved',
          message: `Request resolved: ${data.request_id}`,
          timestamp: new Date()
        }]);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setWsConnected(false);
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setWsConnected(false);
    };
    
    // Heartbeat to keep connection alive
    const heartbeat = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'ping' }));
      }
    }, 30000);
    
    return () => {
      clearInterval(heartbeat);
      ws.close();
    };
  }, []);
  
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        
        {/* Connection Status */}
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  wsConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  <span className={`w-2 h-2 rounded-full mr-1.5 ${
                    wsConnected ? 'bg-green-400' : 'bg-red-400'
                  }`}></span>
                  {wsConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              
              {/* Notifications */}
              {notifications.length > 0 && (
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">
                    {notifications.length} new notification{notifications.length !== 1 ? 's' : ''}
                  </span>
                  <button
                    onClick={() => setNotifications([])}
                    className="text-sm text-primary-600 hover:text-primary-700"
                  >
                    Clear
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
        
        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/pending" element={<PendingRequests />} />
            <Route path="/history" element={<RequestHistory />} />
            <Route path="/knowledge" element={<KnowledgeBase />} />
            <Route path="/simulator" element={<CallSimulator />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
