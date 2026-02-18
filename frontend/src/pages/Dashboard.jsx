import React, { useEffect } from 'react'
import { FiZap, FiCheckCircle, FiTrendingUp, FiType } from 'react-icons/fi'
import { apiService } from '../services/api'
import { useStore } from '../store'

export default function Dashboard() {
  const setBackendConnected = useStore((state) => state.setBackendConnected)
  const setOllamaStatus = useStore((state) => state.setOllamaStatus)

  useEffect(() => {
    apiService
      .healthCheck()
      .then(() => {
        setBackendConnected(true)
        setOllamaStatus(true)
      })
      .catch(() => {
        setBackendConnected(false)
        setOllamaStatus(false)
      })
  }, [setBackendConnected, setOllamaStatus])

  return (
    <div className="space-y-6">
      <div className="glass-card-hover p-8 rounded-2xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
          <div>
            <h1 className="gradient-text text-4xl font-bold mb-4">TalentVector AI</h1>
            <p className="text-slate-300 text-lg leading-relaxed mb-6">
              Transform resumes and job descriptions into structured intelligence using AI-powered semantic matching. 
              Get accurate candidate-job fit analysis powered by advanced embeddings and reinforcement learning.
            </p>
            <div className="flex gap-3">
              <button className="btn-primary">Start Matching</button>
              <button className="btn-secondary">Learn More</button>
            </div>
          </div>
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-xl blur-3xl opacity-20 animate-pulse" />
            <div className="relative glass-card p-8 rounded-xl">
              <FiZap className="w-16 h-16 text-cyan-400 mx-auto mb-4" />
              <p className="text-center text-slate-400 text-sm font-medium">
                AI-powered semantic matching engine
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            icon: FiType,
            title: 'Resume Intelligence',
            description: 'Extract structured candidate profiles with AI',
          },
          {
            icon: FiCheckCircle,
            title: 'Smart Matching',
            description: 'Find perfect candidate-job fits with semantic understanding',
          },
          {
            icon: FiTrendingUp,
            title: 'AI Screening',
            description: 'Evaluate candidates with role-specific AI questions',
          },
        ].map((feature, idx) => {
          const Icon = feature.icon
          return (
            <div key={idx} className="glass-card-hover p-6 rounded-xl">
              <Icon className="w-8 h-8 text-cyan-400 mb-4" />
              <h3 className="text-white font-semibold mb-2">{feature.title}</h3>
              <p className="text-slate-400 text-sm">{feature.description}</p>
            </div>
          )
        })}
      </div>
    </div>
  )
}
