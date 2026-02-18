import React, { useState } from 'react'
import { FiUploadCloud, FiX, FiFile } from 'react-icons/fi'
import { apiService } from '../services/api'
import { useStore } from '../store'
import { extractTextFromFile } from '../utils/pdfParser'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'

export default function ResumeIntelligence() {
  const [resumeText, setResumeText] = useState('')
  const [isDragging, setIsDragging] = useState(false)
  const [activeTab, setActiveTab] = useState('upload')
  const [uploadedFileName, setUploadedFileName] = useState('')

  const loading = useStore((state) => state.loading)
  const setLoading = useStore((state) => state.setLoading)
  const candidateProfile = useStore((state) => state.candidateProfile)
  const setCandidateProfile = useStore((state) => state.setCandidateProfile)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)
  const success = useStore((state) => state.success)
  const setSuccess = useStore((state) => state.setSuccess)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = e.dataTransfer.files
    if (files[0]) {
      handleFileUpload(files[0])
    }
  }

  const handleFileUpload = async (file) => {
    setLoading(true)
    setError(null)
    
    try {
      const text = await extractTextFromFile(file)
      setResumeText(text)
      setUploadedFileName(file.name)
      setSuccess(`Resume "${file.name}" uploaded successfully!`)
    } catch (err) {
      setError(err.message || 'Failed to process file')
    } finally {
      setLoading(false)
    }
  }

  const handleExtractIntelligence = async () => {
    if (!resumeText.trim()) {
      setError('Please paste resume content or upload a file')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await apiService.parseResume(resumeText)
      const profile = response.data.candidate_profile
      setCandidateProfile(profile)
      setSuccess('Candidate intelligence extracted successfully!')
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to extract candidate intelligence'
      console.error('Resume extraction error:', errorMsg)
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">📄 Resume Intelligence</h1>
        <p className="text-slate-400">Extract candidate profiles from resumes</p>
      </div>

      {error && (
        <Alert
          type="error"
          title="Error"
          message={error}
          onClose={() => setError(null)}
        />
      )}

      {success && (
        <Alert
          type="success"
          title="Success"
          message={success}
          onClose={() => setSuccess(null)}
        />
      )}

      <div className="flex gap-4 border-b border-slate-700">
        <button
          onClick={() => setActiveTab('upload')}
          className={`px-6 py-3 font-medium text-sm transition-colors ${
            activeTab === 'upload'
              ? 'text-cyan-400 border-b-2 border-cyan-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          Upload File
        </button>
        <button
          onClick={() => setActiveTab('paste')}
          className={`px-6 py-3 font-medium text-sm transition-colors ${
            activeTab === 'paste'
              ? 'text-cyan-400 border-b-2 border-cyan-400'
              : 'text-slate-400 hover:text-slate-300'
          }`}
        >
          Paste Text
        </button>
      </div>

      {activeTab === 'upload' && (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`glass-card-hover p-12 rounded-xl border-2 border-dashed transition-all ${
            isDragging
              ? 'border-cyan-400 bg-slate-800/50 scale-105'
              : 'border-slate-600'
          }`}
        >
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="text-5xl">
              <FiUploadCloud className="w-16 h-16 text-cyan-400 mx-auto" />
            </div>
            <div className="text-center">
              <h3 className="text-white font-semibold text-lg mb-2">Upload Your Resume</h3>
              <p className="text-slate-400 text-sm mb-4">
                Drag and drop a PDF, DOCX, or TXT file here, or click to browse
              </p>
            </div>
            <label className="btn-primary cursor-pointer">
              Browse Files
              <input
                type="file"
                hidden
                accept=".pdf,.docx,.txt"
                onChange={(e) => e.target.files[0] && handleFileUpload(e.target.files[0])}
              />
            </label>

            {uploadedFileName && (
              <div className="mt-4 p-3 bg-green-600/20 border border-green-600/50 rounded-lg flex items-center gap-2">
                <FiFile className="text-green-400" />
                <span className="text-green-300 text-sm">
                  Loaded: {uploadedFileName}
                </span>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === 'paste' && (
        <div className="space-y-4">
          <div className="glass-card-hover p-4 rounded-xl">
            <textarea
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste your resume content here..."
              className="w-full h-80 bg-slate-900 text-slate-200 border border-slate-600 rounded-lg p-4 focus:outline-none focus:border-cyan-400 transition-colors resize-none"
            />
          </div>
          <div className="flex justify-between items-center">
            <p className="text-xs text-slate-500">
              {resumeText.length} characters entered
            </p>
            {resumeText && (
              <button
                onClick={() => {
                  setResumeText('')
                  setUploadedFileName('')
                }}
                className="flex items-center gap-2 text-slate-400 hover:text-slate-300 transition-colors"
              >
                <FiX className="w-4 h-4" />
                Clear
              </button>
            )}
          </div>
        </div>
      )}

      {loading && (
        <div className="glass-card p-8 rounded-xl flex justify-center">
          <LoadingSpinner text="Processing resume with AI..." />
        </div>
      )}

      {!loading && (
        <button
          onClick={handleExtractIntelligence}
          disabled={!resumeText.trim()}
          className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed text-lg py-4"
        >
          ✨ Extract Candidate Intelligence
        </button>
      )}

      {candidateProfile && !loading && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold text-white border-t border-slate-700 pt-6">
            Candidate Intelligence Profile
          </h2>

          <div className="glass-card-hover p-6 rounded-xl">
            <h3 className="text-lg font-semibold text-white mb-4">👤 Contact Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-slate-500 text-sm">Name</p>
                <p className="text-white font-semibold">{candidateProfile.name || 'N/A'}</p>
              </div>
              <div>
                <p className="text-slate-500 text-sm">Email</p>
                <p className="text-white font-semibold">{candidateProfile.email || 'N/A'}</p>
              </div>
              <div>
                <p className="text-slate-500 text-sm">Phone</p>
                <p className="text-white font-semibold">{candidateProfile.phone || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
