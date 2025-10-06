import { Recommendation } from '../../types/stats';
import { CheckCircle2, Circle } from 'lucide-react';
import { useState } from 'react';

interface RecommendationCardProps {
  recommendation: Recommendation;
  onProgressUpdate?: (id: string, progress: number) => void;
}

export default function RecommendationCard({ recommendation, onProgressUpdate }: RecommendationCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getDifficultyColor = () => {
    switch (recommendation.difficulty) {
      case 'easy':
        return 'bg-green-500/20 text-green-500';
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-500';
      case 'hard':
        return 'bg-red-500/20 text-red-500';
      default:
        return 'bg-gray-500/20 text-gray-500';
    }
  };

  const getImpactColor = () => {
    switch (recommendation.estimated_impact) {
      case 'high':
        return 'text-green-500';
      case 'medium':
        return 'text-yellow-500';
      case 'low':
        return 'text-gray-500';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <div className="bg-lol-dark-lighter rounded-xl p-6 border border-lol-gold/10 hover:border-lol-gold/30 transition-all">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h4 className="font-bold text-white">{recommendation.title}</h4>
            {recommendation.completed && (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            )}
          </div>
          <p className="text-gray-400 text-sm mb-3">{recommendation.description}</p>
        </div>
      </div>

      {/* Badges */}
      <div className="flex gap-2 mb-4">
        <span className={`text-xs px-3 py-1 rounded-full font-medium ${getDifficultyColor()}`}>
          {recommendation.difficulty.toUpperCase()}
        </span>
        <span className={`text-xs px-3 py-1 rounded-full font-medium ${getImpactColor()}`}>
          {recommendation.estimated_impact.toUpperCase()} IMPACT
        </span>
        <span className="text-xs px-3 py-1 rounded-full font-medium bg-lol-blue/20 text-lol-blue">
          {recommendation.category.replace('_', ' ').toUpperCase()}
        </span>
      </div>

      {/* Progress Bar */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Progress</span>
          <span className="text-sm font-bold text-lol-gold">{recommendation.progress}%</span>
        </div>
        <div className="w-full bg-lol-dark rounded-full h-2">
          <div
            className="bg-gradient-to-r from-lol-gold to-lol-gold-light h-2 rounded-full transition-all duration-500"
            style={{ width: `${recommendation.progress}%` }}
          />
        </div>
      </div>

      {/* Expand/Collapse Button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="text-lol-gold text-sm font-medium hover:text-lol-gold-light transition-colors mb-4"
      >
        {isExpanded ? '▼ Show Less' : '▶ Show More'}
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="space-y-4 pt-4 border-t border-gray-700">
          {/* Rationale */}
          <div>
            <p className="text-sm font-medium text-gray-400 mb-2">Why This Matters:</p>
            <p className="text-sm text-gray-300">{recommendation.rationale}</p>
          </div>

          {/* Steps */}
          <div>
            <p className="text-sm font-medium text-gray-400 mb-3">Action Steps:</p>
            <div className="space-y-2">
              {recommendation.steps.map((step, idx) => (
                <div key={idx} className="flex items-start gap-3">
                  <Circle className="w-4 h-4 mt-0.5 text-gray-500 flex-shrink-0" />
                  <span className="text-sm text-gray-300">{step}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Expected Outcome */}
          <div className="bg-lol-dark rounded-lg p-4">
            <p className="text-sm font-medium text-lol-gold mb-2">Expected Outcome:</p>
            <p className="text-sm text-gray-300">{recommendation.expected_outcome}</p>
          </div>

          {/* Action Buttons */}
          {!recommendation.completed && (
            <div className="flex gap-2">
              <button
                onClick={() => onProgressUpdate?.(recommendation.id, Math.min(100, recommendation.progress + 20))}
                className="flex-1 bg-lol-gold hover:bg-lol-gold-light text-lol-dark font-bold py-2 px-4 rounded-lg transition-colors"
              >
                Update Progress
              </button>
              <button
                onClick={() => onProgressUpdate?.(recommendation.id, 100)}
                className="flex-1 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded-lg transition-colors"
              >
                Mark Complete
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
