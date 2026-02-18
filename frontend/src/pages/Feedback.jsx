import React, { useState } from 'react'
import { FiThumbsUp, FiThumbsDown } from 'react-icons/fi'
import { apiService } from '../services/api'
import { useStore } from '../store'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'

export default function Feedback() {
  const [notes, setNotes] = useState('')
  
  const loading = useStore((state) => state.loading)
  const setLoading = useStore((state) => state.setLoading)
  const candidateProfile = useStore((state) => state.candidateProfile)
  const matchResult = useStore((state) => state.matchResult)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)
  const success = useStore((state) => state.success)
  const setSuccess = useStore((state) => state.setSuccess)

  const handleSubmitFeedback = async (isFit) => {
    if (!candidateProfile || !matchResult) {
      setError('Please complete match analysis first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      await apiService.submitFeedback(
        candidateProfile.name || 'Unknown',
        'system',
        matchResult.overall_score || 0,
        isFit ? 'Good Fit' : 'Not Fit',
        notes
      )
      setSuccess('Feedback recorded! System is learning...')
      setNotes('')
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit feedback')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-white">📈 Feedback & Learning</h1>

      {error && <Alert type="error" title="Error" message={error} onClose={() => setError(null)} />}
      {success && <Alert type="success" title="Success" message={success} onClose={() => setSuccess(null)} />}

      <div className="glass-card-hover p-6 rounded-xl">
        <p className="text-slate-500 mb-2">Candidate:</p>
        <p className="text-white font-semibold">{candidateProfile?.name || 'N/A'}</p>
      </div>

      <div className="glass-card-hover p-6 rounded-xl">
        <label className="block text-white font-semibold mb-3">Notes (Optional)</label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Add any feedback or notes about this candidate..."
          className="w-full h-32 bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 resize-none"
        />
      </div>

      {loading ? (
        <LoadingSpinner text="Submitting feedback..." />
      ) : (
        <div className="flex gap-4">
          <button
            onClick={() => handleSubmitFeedback(true)}
            disabled={!candidateProfile}
            className="flex-1 btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <FiThumbsUp /> Good Fit
          </button>
          <button
            onClick={() => handleSubmitFeedback(false)}
            disabled={!candidateProfile}
            className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <FiThumbsDown /> Not Fit
          </button>
        </div>
      )}
    </div>
  )
}
