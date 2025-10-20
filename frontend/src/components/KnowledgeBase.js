import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config';

function KnowledgeBase() {
  const [knowledge, setKnowledge] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  const [newEntry, setNewEntry] = useState({ question: '', answer: '', tags: '' });
  
  useEffect(() => {
    fetchKnowledge();
  }, []);
  
  const fetchKnowledge = async () => {
    try {
      const res = await axios.get(API_ENDPOINTS.ALL_KNOWLEDGE);
      setKnowledge(res.data.knowledge);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };
  
  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchKnowledge();
      return;
    }
    
    try {
      const res = await axios.get(`${API_ENDPOINTS.SEARCH_KNOWLEDGE}?query=${encodeURIComponent(searchQuery)}`);
      setKnowledge(res.data.results);
    } catch (err) {
      alert(`Search error: ${err.message}`);
    }
  };
  
  const handleAddKnowledge = async (e) => {
    e.preventDefault();
    
    if (!newEntry.question.trim() || !newEntry.answer.trim()) {
      alert('Please fill in both question and answer');
      return;
    }
    
    try {
      const tags = newEntry.tags.split(',').map(t => t.trim()).filter(t => t);
      await axios.post(API_ENDPOINTS.ADD_KNOWLEDGE, {
        question: newEntry.question,
        answer: newEntry.answer,
        source: 'manual',
        tags
      });
      
      setNewEntry({ question: '', answer: '', tags: '' });
      setShowAddForm(false);
      await fetchKnowledge();
      alert('Knowledge added successfully!');
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };
  
  const filteredKnowledge = knowledge;
  
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
        <p className="text-red-800">Error loading knowledge base: {error}</p>
      </div>
    );
  }
  
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Knowledge Base</h2>
        <p className="mt-2 text-sm text-gray-600">
          {knowledge.length} learned answer{knowledge.length !== 1 ? 's' : ''} in the system
        </p>
      </div>
      
      {/* Search and Add */}
      <div className="mb-6 space-y-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Search knowledge base..."
              className="w-full border border-gray-300 rounded-md shadow-sm p-3 focus:ring-primary-500 focus:border-primary-500"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-6 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            Search
          </button>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-6 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            {showAddForm ? 'Cancel' : 'Add New'}
          </button>
        </div>
        
        {showAddForm && (
          <form onSubmit={handleAddKnowledge} className="bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Knowledge</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Question
                </label>
                <input
                  type="text"
                  value={newEntry.question}
                  onChange={(e) => setNewEntry({ ...newEntry, question: e.target.value })}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="What question does this answer?"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Answer
                </label>
                <textarea
                  value={newEntry.answer}
                  onChange={(e) => setNewEntry({ ...newEntry, answer: e.target.value })}
                  rows={4}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="Enter the answer..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Tags (comma-separated)
                </label>
                <input
                  type="text"
                  value={newEntry.tags}
                  onChange={(e) => setNewEntry({ ...newEntry, tags: e.target.value })}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., pricing, services, hours"
                />
              </div>
              <button
                type="submit"
                className="w-full px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                Add Knowledge
              </button>
            </div>
          </form>
        )}
      </div>
      
      {/* Knowledge List */}
      {filteredKnowledge.length === 0 ? (
        <div className="bg-white shadow rounded-lg p-12 text-center">
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No knowledge entries</h3>
          <p className="text-gray-600">Start by adding some knowledge or let the AI learn from supervisor responses.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredKnowledge.map((entry) => (
            <div
              key={entry.id}
              className="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      entry.source === 'supervisor' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {entry.source}
                    </span>
                    {entry.usage_count > 0 && (
                      <span className="text-sm text-gray-500">
                        Used {entry.usage_count} time{entry.usage_count !== 1 ? 's' : ''}
                      </span>
                    )}
                  </div>
                  <span className="text-sm text-gray-500">
                    {new Date(entry.created_at?._seconds * 1000 || Date.now()).toLocaleDateString()}
                  </span>
                </div>
                
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Q: {entry.question}
                </h3>
                
                <div className="bg-gray-50 rounded-lg p-4 mb-3">
                  <p className="text-sm text-gray-800">
                    <strong>A:</strong> {entry.answer}
                  </p>
                </div>
                
                {entry.tags && entry.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {entry.tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-primary-100 text-primary-800"
                      >
                        #{tag}
                      </span>
                    ))}
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

export default KnowledgeBase;
