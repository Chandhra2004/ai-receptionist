import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config';

function RequestHistory() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, resolved, unresolved
  
  useEffect(() => {
    fetchAllRequests();
  }, []);
  
  const fetchAllRequests = async () => {
    try {
      const res = await axios.get(API_ENDPOINTS.ALL_REQUESTS);
      setRequests(res.data.requests);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };
  
  const filteredRequests = requests.filter(req => {
    if (filter === 'all') return true;
    return req.status === filter;
  });
  
  const getStatusBadge = (status) => {
    const badges = {
      pending: 'bg-yellow-100 text-yellow-800',
      resolved: 'bg-green-100 text-green-800',
      unresolved: 'bg-red-100 text-red-800',
    };
    return badges[status] || 'bg-gray-100 text-gray-800';
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
        <p className="text-red-800">Error loading history: {error}</p>
      </div>
    );
  }
  
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Request History</h2>
        <p className="mt-2 text-sm text-gray-600">
          Complete history of all help requests
        </p>
      </div>
      
      {/* Filter Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            {['all', 'resolved', 'unresolved', 'pending'].map((tab) => (
              <button
                key={tab}
                onClick={() => setFilter(tab)}
                className={`${
                  filter === tab
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm capitalize`}
              >
                {tab}
                <span className="ml-2 py-0.5 px-2 rounded-full text-xs bg-gray-100">
                  {requests.filter(r => tab === 'all' || r.status === tab).length}
                </span>
              </button>
            ))}
          </nav>
        </div>
      </div>
      
      {/* Requests List */}
      {filteredRequests.length === 0 ? (
        <div className="bg-white shadow rounded-lg p-12 text-center">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No requests found</h3>
          <p className="text-gray-600">No {filter} requests to display.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredRequests.map((request) => (
            <div
              key={request.id}
              className="bg-white shadow rounded-lg overflow-hidden"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadge(request.status)}`}>
                      {request.status}
                    </span>
                    <span className="text-sm text-gray-500">
                      Customer: {request.customer_id}
                    </span>
                  </div>
                  <span className="text-sm text-gray-500">
                    {new Date(request.created_at?._seconds * 1000 || Date.now()).toLocaleString()}
                  </span>
                </div>
                
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  {request.question}
                </h3>
                
                {request.supervisor_answer && (
                  <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-start">
                      <div className="flex-shrink-0">
                        <span className="text-2xl">💬</span>
                      </div>
                      <div className="ml-3 flex-1">
                        <h4 className="text-sm font-medium text-green-900 mb-1">
                          Supervisor Response
                        </h4>
                        <p className="text-sm text-green-800">
                          {request.supervisor_answer}
                        </p>
                        {request.supervisor_id && (
                          <p className="text-xs text-green-600 mt-2">
                            By: {request.supervisor_id}
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
                
                {request.resolved_at && (
                  <p className="text-sm text-gray-500 mt-3">
                    Resolved: {new Date(request.resolved_at?._seconds * 1000 || Date.now()).toLocaleString()}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default RequestHistory;
