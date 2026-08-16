import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function WorkflowStatus() {
  const [threadId, setThreadId] = useState(() => {
    return localStorage.getItem('workflow_status_thread') || ''
  })
  const [result, setResult] = useState(() => {
    const saved = localStorage.getItem('workflow_status_result')
    return saved ? JSON.parse(saved) : null
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Persist threadId
  useEffect(() => {
    localStorage.setItem('workflow_status_thread', threadId)
  }, [threadId])

  // Persist result
  useEffect(() => {
    if (result) {
      localStorage.setItem('workflow_status_result', JSON.stringify(result))
    } else {
      localStorage.removeItem('workflow_status_result')
    }
  }, [result])

  const handleCheck = async (e) => {
    e.preventDefault()
    if (!threadId.trim()) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const data = await api.workflowStatus(threadId.trim())
      setResult(data)
    } catch (err) {
      setError(err.message || 'Failed to fetch status')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <h1 className="page-title">Workflow Status</h1>
      <p className="page-subtitle">Check the status of a procurement workflow by thread ID</p>

      <div className="form-card">
        <form onSubmit={handleCheck}>
          {error && <div className="auth-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="threadId">Thread ID</label>
            <input
              id="threadId"
              type="text"
              value={threadId}
              onChange={(e) => setThreadId(e.target.value)}
              placeholder="Enter thread ID (e.g. abc-123-def-456)"
              required
            />
          </div>

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Checking...' : 'Check Status'}
          </button>
        </form>
      </div>

      {result && (
        <div className="result-panel">
          <h3>
            {result.paused ? '⏸️ Paused' : '✅ Complete'}{' '}
            {result.waiting_at?.length > 0 && (
              <span className="badge badge-pending">at: {result.waiting_at.join(', ')}</span>
            )}
          </h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
