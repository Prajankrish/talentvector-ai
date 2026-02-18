import React from 'react'
import { FiZap } from 'react-icons/fi'
import { useStore } from '../store'

export default function Navbar() {
  const backendConnected = useStore((state) => state.backendConnected)
  const ollamaStatus = useStore((state) => state.ollamaStatus)

  return (
    <nav className="fixed top-0 left-0 right-0 glass-card m-4 mx-auto max-w-7xl z-50 rounded-full">
      <div className="flex items-center justify-between px-6 py-3">
        {/* Logo */}
        <div className="flex items-center gap-2">
          <FiZap className="w-6 h-6 text-cyan-400" />
          <h1 className="gradient-text font-bold text-xl">TalentVector AI</h1>
        </div>

        {/* Status indicators */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                backendConnected ? 'bg-emerald-500' : 'bg-red-500'
              }`}
            />
            <span className="text-xs text-slate-400">
              {backendConnected ? 'Backend Active' : 'Backend Offline'}
            </span>
          </div>

          <div className="w-px h-4 bg-slate-600" />

          <div className="flex items-center gap-2">
            <div
              className={`w-2 h-2 rounded-full ${
                ollamaStatus ? 'bg-emerald-500' : 'bg-red-500'
              }`}
            />
            <span className="text-xs text-slate-400">
              {ollamaStatus ? 'Ollama Connected' : 'Ollama Offline'}
            </span>
          </div>
        </div>
      </div>
    </nav>
  )
}
