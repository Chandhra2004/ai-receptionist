import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);
  
  const fetchStats = async () => {
    try {
      const response = await axios.get(API_ENDPOINTS.STATS);
      setStats(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
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
        <p className="text-red-800">Error loading dashboard: {error}</p>
        <button
          onClick={fetchStats}
          className="mt-2 text-sm text-red-600 hover:text-red-700 underline"
        >
          Retry
        </button>
      </div>
    );
  }
  
  const statCards = [
    {
      title: 'Total Requests',
      value: stats?.total_requests || 0,
      icon: '📊',
      color: 'bg-blue-500',
    },
    {
      title: 'Pending Requests',
      value: stats?.pending_requests || 0,
      icon: '⏳',
      color: 'bg-yellow-500',
    },
    {
      title: 'Resolved Requests',
      value: stats?.resolved_requests || 0,
      icon: '✅',
      color: 'bg-green-500',
    },
    {
      title: 'Knowledge Base',
      value: stats?.knowledge_base_size || 0,
      icon: '📚',
      color: 'bg-purple-500',
    },
    {
      title: 'Active Calls',
      value: stats?.active_calls || 0,
      icon: '📞',
      color: 'bg-indigo-500',
    },
    {
      title: 'Unresolved',
      value: stats?.unresolved_requests || 0,
      icon: '❌',
      color: 'bg-red-500',
    },
  ];
  
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <p className="mt-2 text-sm text-gray-600">
          Overview of your AI receptionist system
        </p>
      </div>
      
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {statCards.map((card, index) => (
          <div
            key={index}
            className="bg-white overflow-hidden shadow rounded-lg hover:shadow-lg transition-shadow"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className={`flex-shrink-0 ${card.color} rounded-md p-3`}>
                  <span className="text-2xl">{card.icon}</span>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {card.title}
                    </dt>
                    <dd className="text-3xl font-semibold text-gray-900">
                      {card.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      
      {/* Quick Actions */}
      <div className="mt-8">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <a
            href="/pending"
            className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow text-center"
          >
            <div className="text-3xl mb-2">🔔</div>
            <div className="text-sm font-medium text-gray-900">View Pending</div>
          </a>
          <a
            href="/simulator"
            className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow text-center"
          >
            <div className="text-3xl mb-2">📞</div>
            <div className="text-sm font-medium text-gray-900">Simulate Call</div>
          </a>
          <a
            href="/knowledge"
            className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow text-center"
          >
            <div className="text-3xl mb-2">📚</div>
            <div className="text-sm font-medium text-gray-900">Knowledge Base</div>
          </a>
          <a
            href="/history"
            className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow text-center"
          >
            <div className="text-3xl mb-2">📜</div>
            <div className="text-sm font-medium text-gray-900">View History</div>
          </a>
        </div>
      </div>
      
      {/* System Status */}
      <div className="mt-8 bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">AI Agent</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span className="w-2 h-2 rounded-full bg-green-400 mr-1.5"></span>
              Online
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Database</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span className="w-2 h-2 rounded-full bg-green-400 mr-1.5"></span>
              Connected
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">LiveKit</span>
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              <span className="w-2 h-2 rounded-full bg-green-400 mr-1.5"></span>
              Ready
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
