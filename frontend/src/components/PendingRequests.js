import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config';

function PendingRequests() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [response, setResponse] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  useEffect(() => {
    fetchPendingRequests();
    const interval = setInterval(fetchPendingRequests, 3000); // Refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);
  
  const fetchPendingRequests = async () => {
    try {
      const res = await axios.get(API_ENDPOINTS.PENDING_REQUESTS);
      setRequests(res.data.requests);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };
  
  const handleRespond = async (requestId) => {
    if (!response.trim()) {
      alert('Please enter a response');
      return;
    }
    
    setSubmitting(true);
    try {
      await axios.post(API_ENDPOINTS.RESPOND_REQUEST, {
        request_id: requestId,
        supervisor_answer: response,
        supervisor_id: 'supervisor_1'
      });
      
      // Clear form and refresh
      setResponse('');
      setSelectedRequest(null);
      await fetchPendingRequests();
      
      alert('Response sent successfully! Customer will be notified.');
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">Error loading requests: {error}</p>
      </div>
    );
  }
  
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Pending Requests</h2>
        <p className="mt-2 text-sm text-gray-600">
          {requests.length} request{requests.length !== 1 ? 's' : ''} waiting for your response
        </p>
      </div>
      
      {requests.length === 0 ? (
        <div className="bg-white shadow rounded-lg p-12 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">All caught up!</h3>
          <p className="text-gray-600">No pending requests at the moment.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {requests.map((request) => (
            <div
              key={request.id}
              className="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                        Pending
                      </span>
                      <span className="ml-2 text-sm text-gray-500">
                        Customer: {request.customer_id}
                      </span>
                      {request.customer_phone && (
                        <span className="ml-2 text-sm text-gray-500">
                          📞 {request.customer_phone}
                        </span>
                      )}
                    </div>
                    
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      {request.question}
                    </h3>
                    
                    <p className="text-sm text-gray-500">
                      Received: {new Date(request.created_at?._seconds * 1000 || Date.now()).toLocaleString()}
                    </p>
                    
                    {request.context && Object.keys(request.context).length > 0 && (
                      <details className="mt-3">
                        <summary className="text-sm text-gray-600 cursor-pointer hover:text-gray-900">
                          View Context
                        </summary>
                        <pre className="mt-2 text-xs bg-gray-50 p-2 rounded overflow-auto">
                          {JSON.stringify(request.context, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                </div>
                
                {selectedRequest === request.id ? (
                  <div className="mt-4 border-t pt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Your Response
                    </label>
                    <textarea
                      value={response}
                      onChange={(e) => setResponse(e.target.value)}
                      rows={4}
                      className="w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="Enter your response to the customer..."
                    />
                    <div className="mt-3 flex space-x-3">
                      <button
                        onClick={() => handleRespond(request.id)}
                        disabled={submitting}
                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                      >
                        {submitting ? 'Sending...' : 'Send Response'}
                      </button>
                      <button
                        onClick={() => {
                          setSelectedRequest(null);
                          setResponse('');
                        }}
                        className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="mt-4">
                    <button
                      onClick={() => setSelectedRequest(request.id)}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      Respond
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PendingRequests;
