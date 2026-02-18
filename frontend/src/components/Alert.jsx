import React from 'react'
import { FiX, FiAlertCircle, FiCheckCircle, FiInfo } from 'react-icons/fi'

export default function Alert({ type = 'info', title, message, onClose }) {
  const colors = {
    error: 'bg-red-500/10 border-red-500/30 text-red-300',
    success: 'bg-green-500/10 border-green-500/30 text-green-300',
    info: 'bg-blue-500/10 border-blue-500/30 text-blue-300',
  }

  const icons = {
    error: FiAlertCircle,
    success: FiCheckCircle,
    info: FiInfo,
  }

  const Icon = icons[type] || FiInfo
  const colorClass = colors[type] || colors.info

  return (
    <div className={`border rounded-lg p-4 flex items-start gap-3 ${colorClass}`}>
      <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
      <div className="flex-1">
        {title && <p className="font-semibold">{title}</p>}
        <p className="text-sm">{message}</p>
      </div>
      {onClose && (
        <button onClick={onClose} className="flex-shrink-0 mt-0.5">
          <FiX className="w-5 h-5" />
        </button>
      )}
    </div>
  )
}
