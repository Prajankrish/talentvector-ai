import React, { useState } from 'react'
import { useStore } from '../store'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'

export default function Screening() {
  const [numQuestions, setNumQuestions] = useState(4)
  
  const loading = useStore((state) => state.loading)
  const hiringProfile = useStore((state) => state.hiringProfile)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)

  const handleGenerateQuestions = () => {
    if (!hiringProfile) {
      setError('Please generate a job profile first')
      return
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">❓ Screening</h1>
      
      {error && <Alert type="error" title="Error" message={error} onClose={() => setError(null)} />}

      <div className="glass-card-hover p-6 rounded-xl">
        <label className="block text-white font-semibold mb-3">Number of Questions</label>
        <input
          type="number"
          value={numQuestions}
          onChange={(e) => setNumQuestions(parseInt(e.target.value))}
          min="1"
          max="10"
          className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
        />
      </div>

      {loading ? (
        <LoadingSpinner text="Generating questions..." />
      ) : (
        <button
          onClick={handleGenerateQuestions}
          disabled={!hiringProfile}
          className="btn-primary w-full disabled:opacity-50"
        >
          Generate Questions
        </button>
      )}
    </div>
  )
}
