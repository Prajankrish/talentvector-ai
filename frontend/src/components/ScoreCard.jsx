import React from 'react'

export default function ScoreCard({ label, score, max = 100, type = 'percentage' }) {
  const percentage = (score / max) * 100

  const getColor = (percentage) => {
    if (percentage >= 75) return 'from-emerald-500 to-emerald-600'
    if (percentage >= 50) return 'from-amber-500 to-amber-600'
    return 'from-red-500 to-red-600'
  }

  const getTextColor = (percentage) => {
    if (percentage >= 75) return 'text-emerald-400'
    if (percentage >= 50) return 'text-amber-400'
    return 'text-red-400'
  }

  return (
    <div className="glass-card p-6 flex flex-col">
      <p className="text-slate-400 text-sm font-medium mb-4">{label}</p>

      <div className="flex-1 flex items-center justify-center mb-4">
        <div className="relative w-32 h-32">
          {/* Background circle */}
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke="currentColor"
              strokeWidth="8"
              className="text-slate-700"
            />
            {/* Progress circle */}
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="8"
              strokeDasharray={`${(percentage / 100) * 339.29} 339.29`}
              strokeLinecap="round"
              className="transition-all duration-500"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#06b6d4" />
                <stop offset="100%" stopColor="#7c3aed" />
              </linearGradient>
            </defs>
          </svg>

          {/* Center text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <p className={`text-3xl font-bold ${getTextColor(percentage)}`}>
              {type === 'percentage' ? `${Math.round(percentage)}%` : `${score.toFixed(1)}`}
            </p>
            <p className="text-xs text-slate-500 mt-1">{type === 'percentage' ? 'Match' : 'Score'}</p>
          </div>
        </div>
      </div>

      {/* Details */}
      <div className="text-center">
        <p className="text-xs text-slate-500">
          {percentage >= 75 ? '🟢 Strong Match' : percentage >= 50 ? '🟡 Moderate Match' : '🔴 Weak Match'}
        </p>
      </div>
    </div>
  )
}
