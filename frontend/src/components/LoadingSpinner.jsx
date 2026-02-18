import React from 'react'

export default function LoadingSpinner({ size = 'md', text = 'Loading...' }) {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  }

  return (
    <div className="flex flex-col items-center justify-center gap-4">
      <div
        className={`${sizeClasses[size]} rounded-full border-2 border-slate-700 border-t-cyan-400 animate-spin`}
      />
      <p className="text-slate-400 text-sm">{text}</p>
    </div>
  )
}
