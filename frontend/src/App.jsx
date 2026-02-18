import React, { useState, useEffect } from 'react'
import { useStore } from './store'
import Navbar from './components/Navbar'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import ResumeIntelligence from './pages/ResumeIntelligence'
import JobIntelligence from './pages/JobIntelligence'
import MatchAnalysis from './pages/MatchAnalysis'
import Screening from './pages/Screening'
import Feedback from './pages/Feedback'
import HiringManager from './pages/HiringManager'
import HiringManagerProfile from './pages/HiringManagerProfile'

export default function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const hiringManager = useStore((state) => state.hiringManager)

  // If not authenticated, show hiring manager page
  if (!hiringManager?.isAuthenticated) {
    return <HiringManager />
  }

  // Map page names to components
  const pages = {
    dashboard: <Dashboard />,
    resume: <ResumeIntelligence />,
    job: <JobIntelligence />,
    match: <MatchAnalysis />,
    screening: <Screening />,
    feedback: <Feedback />,
    hiringManager: <HiringManagerProfile />,
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800">
      <Navbar currentPage={currentPage} />
      <div className="flex">
        <Sidebar currentPage={currentPage} onPageChange={setCurrentPage} />
        <main className="flex-1 p-8 overflow-auto">
          <div className="max-w-7xl mx-auto">
            {pages[currentPage] || pages.dashboard}
          </div>
        </main>
      </div>
    </div>
  )
}
