import { Target, Calendar, CheckCircle2, TrendingUp } from 'lucide-react';

interface Goal {
  id: string;
  title: string;
  description: string;
  category: string;
  target_value?: number;
  target_date?: string;
  current_value?: number;
  progress_percentage: number;
  status: 'in_progress' | 'completed' | 'abandoned';
  ai_checkpoints: string[];
  related_insights: string[];
  created_at: string;
  completed_at?: string;
}

interface GoalTrackerProps {
  goals: Goal[];
}

export default function GoalTracker({ goals }: GoalTrackerProps) {
  const activeGoals = goals.filter((g) => g.status === 'in_progress');
  const completedGoals = goals.filter((g) => g.status === 'completed');

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'rank':
        return '🎯';
      case 'champion_mastery':
        return '⭐';
      case 'stat_improvement':
        return '📈';
      default:
        return '🎮';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const GoalCard = ({ goal }: { goal: Goal }) => (
    <div
      className={`bg-lol-dark-lighter rounded-lg p-5 border ${
        goal.status === 'completed' ? 'border-green-500/30' : 'border-lol-gold/10'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{getCategoryIcon(goal.category)}</span>
          <div>
            <h4 className="font-bold text-white">{goal.title}</h4>
            <p className="text-sm text-gray-400">{goal.description}</p>
          </div>
        </div>
        {goal.status === 'completed' && <CheckCircle2 className="w-6 h-6 text-green-500 flex-shrink-0" />}
      </div>

      {/* Progress */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">Progress</span>
          <span className="text-sm font-bold text-lol-gold">{goal.progress_percentage}%</span>
        </div>
        <div className="w-full bg-lol-dark rounded-full h-2.5">
          <div
            className={`h-2.5 rounded-full transition-all duration-500 ${
              goal.status === 'completed'
                ? 'bg-gradient-to-r from-green-500 to-green-400'
                : 'bg-gradient-to-r from-lol-gold to-lol-gold-light'
            }`}
            style={{ width: `${goal.progress_percentage}%` }}
          />
        </div>
      </div>

      {/* Target Info */}
      {(goal.target_date || goal.target_value) && (
        <div className="flex gap-4 mb-4 text-sm">
          {goal.target_date && (
            <div className="flex items-center gap-2 text-gray-400">
              <Calendar className="w-4 h-4" />
              <span>Target: {formatDate(goal.target_date)}</span>
            </div>
          )}
          {goal.target_value && goal.current_value !== undefined && (
            <div className="flex items-center gap-2 text-gray-400">
              <TrendingUp className="w-4 h-4" />
              <span>
                {goal.current_value} / {goal.target_value}
              </span>
            </div>
          )}
        </div>
      )}

      {/* AI Checkpoints */}
      {goal.ai_checkpoints.length > 0 && (
        <div>
          <p className="text-sm font-medium text-gray-400 mb-2">AI Checkpoints:</p>
          <div className="space-y-1.5">
            {goal.ai_checkpoints.map((checkpoint, idx) => {
              const isComplete = idx < goal.ai_checkpoints.length * (goal.progress_percentage / 100);
              return (
                <div key={idx} className="flex items-start gap-2 text-sm">
                  {isComplete ? (
                    <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                  ) : (
                    <div className="w-4 h-4 border-2 border-gray-600 rounded-full flex-shrink-0 mt-0.5" />
                  )}
                  <span className={isComplete ? 'text-green-400' : 'text-gray-400'}>{checkpoint}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Completion Date */}
      {goal.completed_at && (
        <div className="mt-4 pt-4 border-t border-gray-700">
          <p className="text-sm text-green-400">
            ✓ Completed on {formatDate(goal.completed_at)}
          </p>
        </div>
      )}
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Active Goals */}
      {activeGoals.length > 0 && (
        <div>
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <Target className="w-6 h-6 text-lol-gold" />
            Active Goals ({activeGoals.length})
          </h3>
          <div className="space-y-4">
            {activeGoals.map((goal) => (
              <GoalCard key={goal.id} goal={goal} />
            ))}
          </div>
        </div>
      )}

      {/* Completed Goals */}
      {completedGoals.length > 0 && (
        <div>
          <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-6 h-6 text-green-500" />
            Completed Goals ({completedGoals.length})
          </h3>
          <div className="space-y-4">
            {completedGoals.map((goal) => (
              <GoalCard key={goal.id} goal={goal} />
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {goals.length === 0 && (
        <div className="text-center py-12">
          <Target className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No goals set yet. Create your first goal to start tracking your progress!</p>
        </div>
      )}
    </div>
  );
}
