import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ProgressionTimeSeries } from '../../types/stats';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ProgressionChartProps {
  data: ProgressionTimeSeries;
}

export default function ProgressionChart({ data }: ProgressionChartProps) {
  const formatMetricName = (metric: string) => {
    return metric
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  const getTrendIcon = () => {
    if (data.trend === 'improving') return <TrendingUp className="w-5 h-5 text-green-500" />;
    if (data.trend === 'declining') return <TrendingDown className="w-5 h-5 text-red-500" />;
    return <Minus className="w-5 h-5 text-gray-500" />;
  };

  const getTrendColor = () => {
    if (data.trend === 'improving') return 'text-green-500';
    if (data.trend === 'declining') return 'text-red-500';
    return 'text-gray-500';
  };

  return (
    <div className="bg-lol-dark-lighter rounded-xl p-6 border border-lol-gold/10">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-white mb-1">{formatMetricName(data.metric)}</h3>
          <p className="text-gray-400 text-sm">Over time</p>
        </div>
        <div className="flex items-center gap-2">
          {getTrendIcon()}
          <span className={`font-bold ${getTrendColor()}`}>
            {data.change_percentage && data.change_percentage > 0 ? '+' : ''}
            {data.change_percentage?.toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data.data_points}>
          <CartesianGrid strokeDasharray="3 3" stroke="#31313C" />
          <XAxis
            dataKey="timestamp"
            stroke="#8d99ae"
            tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short' })}
          />
          <YAxis stroke="#8d99ae" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1E2328',
              border: '1px solid #C89B3C',
              borderRadius: '8px',
            }}
            labelFormatter={(value) => new Date(value).toLocaleDateString()}
            formatter={(value: number) => [value.toFixed(2), formatMetricName(data.metric)]}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#C89B3C"
            strokeWidth={3}
            dot={{ fill: '#C89B3C', r: 4 }}
            activeDot={{ r: 6 }}
            name={formatMetricName(data.metric)}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
