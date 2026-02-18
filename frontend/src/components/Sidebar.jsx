import React from 'react'
import { FiHome, FiFileText, FiBriefcase, FiZap, FiHelpCircle, FiBarChart2, FiUser } from 'react-icons/fi'

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: FiHome },
  { id: 'resume', label: 'Resume Intelligence', icon: FiFileText },
  { id: 'job', label: 'Job Intelligence', icon: FiBriefcase },
  { id: 'match', label: 'Match Analysis', icon: FiZap },
  { id: 'screening', label: 'Screening', icon: FiHelpCircle },
  { id: 'feedback', label: 'Feedback & Learning', icon: FiBarChart2 },
  { id: 'hiringManager', label: 'My Profile', icon: FiUser },
]

export default function Sidebar({ currentPage, onPageChange }) {
  return (
    <aside className="fixed left-0 top-24 h-screen w-64 glass-card m-4 rounded-xl p-6 overflow-y-auto">
      <div className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id

          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                isActive
                  ? 'bg-gradient-to-r from-purple-600 to-cyan-600 text-white shadow-lg shadow-purple-500/30'
                  : 'text-slate-300 hover:bg-slate-800/50'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="font-medium text-sm">{item.label}</span>
            </button>
          )
        })}
      </div>

      {/* Footer info */}
      <div className="mt-8 pt-8 border-t border-slate-700/50">
        <p className="text-xs text-slate-500 font-semibold">VERSION 1.0.0</p>
        <p className="text-xs text-slate-600 mt-2">
          AI-native recruiting powered by Mistral
        </p>
      </div>
    </aside>
  )
}
