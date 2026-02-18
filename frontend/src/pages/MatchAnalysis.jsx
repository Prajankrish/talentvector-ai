import React from 'react'
import { useStore } from '../store'

export default function MatchAnalysis() {
  const candidateProfile = useStore((state) => state.candidateProfile)
  const hiringProfile = useStore((state) => state.hiringProfile)

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">🎯 Match Analysis</h1>
      
      <div className="grid grid-cols-2 gap-4">
        <div className="glass-card-hover p-6 rounded-xl">
          <p className="text-slate-500">Candidate</p>
          <p className="text-white font-semibold">{candidateProfile?.name || 'Not loaded'}</p>
        </div>
        <div className="glass-card-hover p-6 rounded-xl">
          <p className="text-slate-500">Job</p>
          <p className="text-white font-semibold">{hiringProfile?.position || 'Not loaded'}</p>
        </div>
      </div>

      {candidateProfile && hiringProfile ? (
        <button className="btn-primary w-full">Analyze Match</button>
      ) : (
        <p className="text-slate-400 text-center">Please load candidate and job profiles first</p>
      )}
    </div>
  )
}
