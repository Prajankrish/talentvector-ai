import React, { useState } from 'react'
import { FiEdit2, FiSave, FiX, FiLogOut } from 'react-icons/fi'
import { useStore } from '../store'
import Alert from '../components/Alert'

export default function HiringManagerProfile() {
  const [isEditing, setIsEditing] = useState(false)
  const [editingData, setEditingData] = useState({})

  const hiringManager = useStore((state) => state.hiringManager)
  const setHiringManager = useStore((state) => state.setHiringManager)
  const setSuccess = useStore((state) => state.setSuccess)
  const success = useStore((state) => state.success)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)

  const handleEdit = () => {
    setEditingData({
      name: hiringManager?.name || '',
      email: hiringManager?.email || '',
      company: hiringManager?.company || '',
      phone: hiringManager?.phone || '',
    })
    setIsEditing(true)
  }

  const handleSave = () => {
    if (!editingData.name.trim() || !editingData.company.trim()) {
      setError('Name and company are required')
      return
    }

    setHiringManager({
      ...hiringManager,
      ...editingData,
      isAuthenticated: true,
    })
    setSuccess('Profile updated successfully!')
    setIsEditing(false)
  }

  const handleCancel = () => {
    setIsEditing(false)
    setEditingData({})
  }

  const handleLogout = () => {
    setHiringManager(null)
    setSuccess('Logged out successfully')
  }

  if (!hiringManager) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex items-center justify-center p-4">
        <div className="glass-card p-8 rounded-2xl max-w-md w-full">
          <p className="text-slate-300 text-center">Please log in first</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">👤 Hiring Manager Profile</h1>
        {!isEditing && (
          <button
            onClick={handleEdit}
            className="btn-primary flex items-center gap-2"
          >
            <FiEdit2 className="w-4 h-4" /> Edit Profile
          </button>
        )}
      </div>

      {error && (
        <Alert type="error" title="Error" message={error} onClose={() => setError(null)} />
      )}
      {success && (
        <Alert type="success" title="Success" message={success} onClose={() => setSuccess(null)} />
      )}

      <div className="glass-card-hover p-8 rounded-2xl">
        {isEditing ? (
          <div className="space-y-6">
            <div>
              <label className="block text-white text-sm font-semibold mb-2">Name</label>
              <input
                type="text"
                value={editingData.name}
                onChange={(e) => setEditingData({ ...editingData, name: e.target.value })}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2">Email</label>
              <input
                type="email"
                value={editingData.email}
                onChange={(e) => setEditingData({ ...editingData, email: e.target.value })}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2">Company</label>
              <input
                type="text"
                value={editingData.company}
                onChange={(e) => setEditingData({ ...editingData, company: e.target.value })}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2">Phone</label>
              <input
                type="tel"
                value={editingData.phone}
                onChange={(e) => setEditingData({ ...editingData, phone: e.target.value })}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={handleSave}
                className="flex-1 btn-primary flex items-center justify-center gap-2"
              >
                <FiSave className="w-4 h-4" /> Save Changes
              </button>
              <button
                onClick={handleCancel}
                className="flex-1 btn-secondary flex items-center justify-center gap-2"
              >
                <FiX className="w-4 h-4" /> Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <p className="text-slate-500 text-sm font-medium">Name</p>
                <p className="text-white text-lg font-semibold mt-1">{hiringManager.name}</p>
              </div>
              <div>
                <p className="text-slate-500 text-sm font-medium">Email</p>
                <p className="text-white text-lg font-semibold mt-1">{hiringManager.email}</p>
              </div>
              <div>
                <p className="text-slate-500 text-sm font-medium">Company</p>
                <p className="text-white text-lg font-semibold mt-1">{hiringManager.company}</p>
              </div>
              <div>
                <p className="text-slate-500 text-sm font-medium">Phone</p>
                <p className="text-white text-lg font-semibold mt-1">{hiringManager.phone || 'Not provided'}</p>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-700">
              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition"
              >
                <FiLogOut className="w-4 h-4" /> Logout
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
