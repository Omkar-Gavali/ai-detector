import * as React from "react"

interface ProgressProps {
  value: number
  className?: string
}

export function Progress({ value, className }: ProgressProps) {
  return (
    <div className={`bg-gray-200 rounded-full overflow-hidden ${className}`}>
      <div 
        className="bg-blue-600 h-full transition-all duration-300 ease-out"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  )
}
