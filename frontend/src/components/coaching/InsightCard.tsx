import { CoachingInsight } from '../../types/stats';
import { AlertCircle, TrendingUp, AlertTriangle, Lightbulb, CheckCircle, Award, Target } from 'lucide-react';

interface InsightCardProps {
  insight: CoachingInsight;
}

export default function InsightCard({ insight }: InsightCardProps) {
  const getTypeIcon = () => {
    switch (insight.type) {
      case 'strength':
        return <Award className="w-5 h-5" />;
      case 'weakness':
        return <AlertCircle className="w-5 h-5" />;
      case 'improvement':
        return <TrendingUp className="w-5 h-5" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5" />;
      case 'tip':
        return <Lightbulb className="w-5 h-5" />;
      case 'pattern':
        return <Target className="w-5 h-5" />;
      case 'achievement':
        return <CheckCircle className="w-5 h-5" />;
      default:
        return <Lightbulb className="w-5 h-5" />;
    }
  };

  const getTypeColor = () => {
    switch (insight.type) {
      case 'strength':
      case 'improvement':
      case 'achievement':
        return 'bg-green-500/10 border-green-500/30 text-green-500';
      case 'weakness':
      case 'warning':
        return 'bg-red-500/10 border-red-500/30 text-red-500';
      case 'tip':
      case 'pattern':
        return 'bg-blue-500/10 border-blue-500/30 text-blue-500';
      default:
        return 'bg-gray-500/10 border-gray-500/30 text-gray-500';
    }
  };

  const getPriorityBadge = () => {
    const colors = {
      critical: 'bg-red-500 text-white',
      high: 'bg-orange-500 text-white',
      medium: 'bg-yellow-500 text-black',
      low: 'bg-gray-500 text-white',
    };

    return (
      <span className={`text-xs px-2 py-1 rounded ${colors[insight.priority]}`}>
        {insight.priority.toUpperCase()}
      </span>
    );
  };

  return (
    <div className={`rounded-xl p-6 border ${getTypeColor()}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {getTypeIcon()}
          <div>
            <h4 className="font-bold text-white mb-1">{insight.title}</h4>
            <p className="text-xs text-gray-400">
              {new Date(insight.generated_at).toLocaleDateString()} · {(insight.confidence_score * 100).toFixed(0)}% confidence
            </p>
          </div>
        </div>
        {getPriorityBadge()}
      </div>

      {/* Description */}
      <p className="text-gray-300 mb-4">{insight.description}</p>

      {/* Evidence */}
      {insight.evidence.length > 0 && (
        <div className="mb-4">
          <p className="text-sm font-medium text-gray-400 mb-2">Evidence:</p>
          <ul className="space-y-1">
            {insight.evidence.map((item, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-lol-gold mt-1">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommended Actions */}
      {insight.actionable && insight.recommended_actions.length > 0 && (
        <div className="bg-lol-dark-light rounded-lg p-4 mt-4">
          <p className="text-sm font-medium text-lol-gold mb-2">💡 Recommended Actions:</p>
          <ul className="space-y-2">
            {insight.recommended_actions.map((action, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-lol-gold mt-1">→</span>
                <span>{action}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
