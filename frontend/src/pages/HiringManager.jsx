import React, { useState } from 'react'
import { FiMail, FiLock, FiUser, FiBriefcase, FiPhone, FiLogOut } from 'react-icons/fi'
import { useStore } from '../store'
import Alert from '../components/Alert'

export default function HiringManager() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [company, setCompany] = useState('')
  const [phone, setPhone] = useState('')

  const hiringManager = useStore((state) => state.hiringManager)
  const setHiringManager = useStore((state) => state.setHiringManager)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)
  const success = useStore((state) => state.success)
  const setSuccess = useStore((state) => state.setSuccess)

  const handleLogin = () => {
    if (!email.trim() || !password.trim()) {
      setError('Please enter email and password')
      return
    }

    setHiringManager({
      email,
      password,
      name: email.split('@')[0],
      company: 'Company',
      isAuthenticated: true,
    })

    setSuccess('Welcome back!')
    setEmail('')
    setPassword('')
  }

  const handleSignUp = () => {
    if (!email.trim() || !password.trim() || !name.trim() || !company.trim()) {
      setError('Please fill in all fields')
      return
    }

    setHiringManager({
      email,
      password,
      name,
      company,
      phone,
      isAuthenticated: true,
    })

    setSuccess('Account created successfully!')
    setEmail('')
    setPassword('')
    setName('')
    setCompany('')
    setPhone('')
  }

  const handleLogout = () => {
    setHiringManager(null)
    setSuccess('Logged out successfully')
  }

  if (hiringManager?.isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex items-center justify-center p-4">
        <div className="glass-card p-8 rounded-2xl max-w-md w-full">
          <h2 className="text-2xl font-bold text-white mb-6">Hiring Manager Dashboard</h2>

          <div className="space-y-4 mb-6">
            <div>
              <p className="text-slate-500 text-sm">Name</p>
              <p className="text-white font-semibold">{hiringManager.name}</p>
            </div>
            <div>
              <p className="text-slate-500 text-sm">Company</p>
              <p className="text-white font-semibold">{hiringManager.company}</p>
            </div>
            <div>
              <p className="text-slate-500 text-sm">Email</p>
              <p className="text-white font-semibold">{hiringManager.email}</p>
            </div>
          </div>

          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-3 rounded-lg transition"
          >
            <FiLogOut /> Logout
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-900 to-slate-800 flex items-center justify-center p-4">
      <div className="glass-card p-8 rounded-2xl max-w-md w-full">
        {error && (
          <Alert type="error" title="Error" message={error} onClose={() => setError(null)} />
        )}
        {success && (
          <Alert type="success" title="Success" message={success} onClose={() => setSuccess(null)} />
        )}

        <h1 className="gradient-text text-3xl font-bold mb-8 text-center">TalentVector AI</h1>

        <div className="flex gap-4 mb-6 border-b border-slate-700">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-3 font-semibold text-sm transition-colors ${
              isLogin
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-3 font-semibold text-sm transition-colors ${
              !isLogin
                ? 'text-cyan-400 border-b-2 border-cyan-400'
                : 'text-slate-400 hover:text-slate-300'
            }`}
          >
            Sign Up
          </button>
        </div>

        {isLogin ? (
          <div className="space-y-4">
            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiMail className="w-4 h-4" /> Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiLock className="w-4 h-4" /> Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <button onClick={handleLogin} className="w-full btn-primary mt-6">
              Login
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiUser className="w-4 h-4" /> Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiBriefcase className="w-4 h-4" /> Company
              </label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Your Company"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiMail className="w-4 h-4" /> Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiPhone className="w-4 h-4" /> Phone (Optional)
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+1 (555) 000-0000"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-semibold mb-2 flex items-center gap-2">
                <FiLock className="w-4 h-4" /> Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>

            <button onClick={handleSignUp} className="w-full btn-primary mt-6">
              Sign Up
            </button>
          </div>
        )}

        <p className="text-center text-slate-500 text-xs mt-6">
          {isLogin ? "Don't have an account? Sign up above" : 'Already have an account? Login above'}
        </p>
      </div>
    </div>
  )
}
