import React, { useState } from 'react';
import axios from 'axios';
import { API_ENDPOINTS } from '../config';

function CallSimulator() {
  const [callData, setCallData] = useState({
    customer_id: '',
    customer_phone: '',
    customer_name: '',
    question: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  
  const sampleQuestions = [
    "What are your hours?",
    "How much does a haircut cost?",
    "Do you offer wedding packages?",
    "Can I book an appointment for tomorrow at 3 PM?",
    "What's your cancellation policy?",
    "Do you have parking available?",
    "Can I get a discount for multiple services?",
    "Do you offer gift certificates?",
  ];
  
  const handleSimulateCall = async (e) => {
    e.preventDefault();
    
    if (!callData.customer_id || !callData.customer_phone || !callData.question) {
      alert('Please fill in all required fields');
      return;
    }
    
    setLoading(true);
    setResult(null);
    
    try {
      const response = await axios.post(API_ENDPOINTS.SIMULATE_CALL, {
        customer_id: callData.customer_id,
        customer_phone: callData.customer_phone,
        customer_name: callData.customer_name || 'Customer',
        question: callData.question
      });
      
      setResult(response.data);
      
      // Clear form after successful simulation
      // setCallData({ customer_id: '', customer_phone: '', customer_name: '', question: '' });
    } catch (err) {
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  const handleQuickFill = () => {
    const randomQuestion = sampleQuestions[Math.floor(Math.random() * sampleQuestions.length)];
    const randomId = `CUST${Math.floor(Math.random() * 10000)}`;
    const randomPhone = `(555) ${Math.floor(Math.random() * 900) + 100}-${Math.floor(Math.random() * 9000) + 1000}`;
    
    setCallData({
      customer_id: randomId,
      customer_phone: randomPhone,
      customer_name: 'Test Customer',
      question: randomQuestion
    });
  };
  
  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Call Simulator</h2>
        <p className="mt-2 text-sm text-gray-600">
          Simulate incoming calls to test the AI receptionist
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Simulation Form */}
        <div>
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-medium text-gray-900">Simulate Call</h3>
              <button
                onClick={handleQuickFill}
                className="text-sm text-primary-600 hover:text-primary-700 underline"
              >
                Quick Fill
              </button>
            </div>
            
            <form onSubmit={handleSimulateCall} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer ID *
                </label>
                <input
                  type="text"
                  value={callData.customer_id}
                  onChange={(e) => setCallData({ ...callData, customer_id: e.target.value })}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="e.g., CUST1234"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer Phone *
                </label>
                <input
                  type="tel"
                  value={callData.customer_phone}
                  onChange={(e) => setCallData({ ...callData, customer_phone: e.target.value })}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="(555) 123-4567"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Customer Name
                </label>
                <input
                  type="text"
                  value={callData.customer_name}
                  onChange={(e) => setCallData({ ...callData, customer_name: e.target.value })}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="John Doe"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Question *
                </label>
                <textarea
                  value={callData.question}
                  onChange={(e) => setCallData({ ...callData, question: e.target.value })}
                  rows={4}
                  className="w-full border border-gray-300 rounded-md shadow-sm p-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="What would the customer like to know?"
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={loading}
                className="w-full px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Simulating Call...
                  </span>
                ) : (
                  '📞 Simulate Call'
                )}
              </button>
            </form>
          </div>
          
          {/* Sample Questions */}
          <div className="mt-6 bg-white shadow rounded-lg p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Sample Questions</h3>
            <div className="space-y-2">
              {sampleQuestions.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => setCallData({ ...callData, question })}
                  className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 rounded border border-gray-200 hover:border-primary-300 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        </div>
        
        {/* Results */}
        <div>
          {result ? (
            <div className="bg-white shadow rounded-lg p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Call Result</h3>
              
              <div className="space-y-4">
                {/* AI Response */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <span className="text-2xl">🤖</span>
                    </div>
                    <div className="ml-3 flex-1">
                      <h4 className="text-sm font-medium text-blue-900 mb-1">
                        AI Agent Response
                      </h4>
                      <p className="text-sm text-blue-800">
                        {result.response}
                      </p>
                    </div>
                  </div>
                </div>
                
                {/* Escalation Status */}
                <div className={`border rounded-lg p-4 ${
                  result.needs_help 
                    ? 'bg-yellow-50 border-yellow-200' 
                    : 'bg-green-50 border-green-200'
                }`}>
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">
                      {result.needs_help ? '⚠️' : '✅'}
                    </span>
                    <div>
                      <h4 className={`text-sm font-medium mb-1 ${
                        result.needs_help ? 'text-yellow-900' : 'text-green-900'
                      }`}>
                        {result.needs_help ? 'Escalated to Supervisor' : 'Handled by AI'}
                      </h4>
                      <p className={`text-sm ${
                        result.needs_help ? 'text-yellow-800' : 'text-green-800'
                      }`}>
                        {result.needs_help 
                          ? 'The AI couldn\'t answer this question and created a help request.'
                          : 'The AI successfully answered the customer\'s question.'}
                      </p>
                    </div>
                  </div>
                </div>
                
                {/* Help Request ID */}
                {result.help_request_id && (
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                    <h4 className="text-sm font-medium text-gray-900 mb-1">
                      Help Request Created
                    </h4>
                    <p className="text-sm text-gray-600 font-mono">
                      ID: {result.help_request_id}
                    </p>
                    <a
                      href="/pending"
                      className="mt-2 inline-block text-sm text-primary-600 hover:text-primary-700 underline"
                    >
                      View in Pending Requests →
                    </a>
                  </div>
                )}
                
                {/* Knowledge Used */}
                {result.knowledge_used && (
                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">📚</span>
                      <div>
                        <h4 className="text-sm font-medium text-purple-900 mb-1">
                          Used Learned Knowledge
                        </h4>
                        <p className="text-sm text-purple-800">
                          The AI used a previously learned answer from the knowledge base.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
                
                {/* Simulate Another */}
                <button
                  onClick={() => setResult(null)}
                  className="w-full px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  Simulate Another Call
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white shadow rounded-lg p-12 text-center">
              <div className="text-6xl mb-4">📞</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Ready to Simulate
              </h3>
              <p className="text-gray-600">
                Fill in the form and click "Simulate Call" to test the AI receptionist.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CallSimulator;
