import { useState } from 'react';
import CoachingChat from '../components/coaching/CoachingChat';
import InsightCard from '../components/coaching/InsightCard';
import RecommendationCard from '../components/coaching/RecommendationCard';
import GoalTracker from '../components/coaching/GoalTracker';
import { mockInsights, mockRecommendations, mockChatMessages, mockGoals } from '../data/mockCoaching';
import { ChatMessage } from '../types/stats';

export default function CoachingPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(mockChatMessages);
  const [activeTab, setActiveTab] = useState<'insights' | 'recommendations' | 'goals'>('insights');

  const handleSendMessage = (content: string) => {
    const newMessage: ChatMessage = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages([...messages, newMessage]);

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: `msg_${Date.now() + 1}`,
        role: 'assistant',
        content: "I'm analyzing your question. In a real implementation, this would call AWS Bedrock to generate a personalized response based on your match data.",
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-black text-white mb-3">AI Coaching</h1>
        <p className="text-xl text-gray-400">Get personalized insights and recommendations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Chat */}
        <div className="lg:col-span-2">
          <CoachingChat messages={messages} onSendMessage={handleSendMessage} isLoading={false} />
        </div>

        {/* Right Column - Insights/Recommendations/Goals */}
        <div className="lg:col-span-1">
          {/* Tabs */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setActiveTab('insights')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === 'insights'
                  ? 'bg-lol-gold text-lol-dark'
                  : 'bg-lol-dark-lighter text-gray-300 hover:bg-lol-dark-light'
              }`}
            >
              Insights
            </button>
            <button
              onClick={() => setActiveTab('recommendations')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === 'recommendations'
                  ? 'bg-lol-gold text-lol-dark'
                  : 'bg-lol-dark-lighter text-gray-300 hover:bg-lol-dark-light'
              }`}
            >
              Actions
            </button>
            <button
              onClick={() => setActiveTab('goals')}
              className={`flex-1 px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === 'goals'
                  ? 'bg-lol-gold text-lol-dark'
                  : 'bg-lol-dark-lighter text-gray-300 hover:bg-lol-dark-light'
              }`}
            >
              Goals
            </button>
          </div>

          {/* Tab Content */}
          <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
            {activeTab === 'insights' && (
              <>
                <h3 className="text-lg font-bold text-white mb-4">Active Insights ({mockInsights.length})</h3>
                {mockInsights.map((insight) => (
                  <InsightCard key={insight.id} insight={insight} />
                ))}
              </>
            )}

            {activeTab === 'recommendations' && (
              <>
                <h3 className="text-lg font-bold text-white mb-4">
                  Recommendations ({mockRecommendations.length})
                </h3>
                {mockRecommendations.map((rec) => (
                  <RecommendationCard
                    key={rec.id}
                    recommendation={rec}
                    onProgressUpdate={(id, progress) => {
                      console.log(`Update ${id} to ${progress}%`);
                    }}
                  />
                ))}
              </>
            )}

            {activeTab === 'goals' && <GoalTracker goals={mockGoals} />}
          </div>
        </div>
      </div>
    </div>
  );
}
