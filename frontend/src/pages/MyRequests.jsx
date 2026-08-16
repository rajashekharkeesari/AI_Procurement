import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function MyRequests() {
  const [requests, setRequests] = useState([])
  const [checking, setChecking] = useState(null)

  useEffect(() => {
    loadRequests()
  }, [])

  const loadRequests = () => {
    const stored = JSON.parse(localStorage.getItem('my_requests') || '[]')
    setRequests(stored)
  }

  const checkStatus = async (threadId, index) => {
    setChecking(index)
    try {
      const data = await api.workflowStatus(threadId)
      const updated = [...requests]
      if (data.paused) {
        updated[index].status = 'awaiting_approval'
      } else {
        const state = data.current_state || {}
        updated[index].status = state.status || 'completed'
        updated[index].comments = state.comments || ''
        updated[index].notification = state.notification || ''
      }
      setRequests(updated)
      localStorage.setItem('my_requests', JSON.stringify(updated))
    } catch {
      const updated = [...requests]
      updated[index].status = 'error'
      setRequests(updated)
      localStorage.setItem('my_requests', JSON.stringify(updated))
    } finally {
      setChecking(null)
    }
  }

  const refreshAll = async () => {
    for (let i = 0; i < requests.length; i++) {
      if (requests[i].thread_id) {
        await checkStatus(requests[i].thread_id, i)
      }
    }
  }

  const clearHistory = () => {
    setRequests([])
    localStorage.removeItem('my_requests')
  }

  const getStatusBadge = (status) => {
    const map = {
      pending: 'badge-pending',
      awaiting_approval: 'badge-pending',
      approved: 'badge-approved',
      ordered: 'badge-ordered',
      rejected: 'badge-rejected',
      completed: 'badge-approved',
      error: 'badge-rejected',
    }
    return map[status] || 'badge-pending'
  }

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 className="page-title">My Requests</h1>
          <p className="page-subtitle" style={{ marginBottom: 0 }}>All your submitted procurement requests</p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {requests.length > 0 && (
            <>
              <button onClick={refreshAll} className="submit-btn" style={{ fontSize: '0.8rem', padding: '0.5rem 1rem' }}>
                Refresh All
              </button>
              <button onClick={clearHistory} style={{ background: '#666', color: '#fff', padding: '0.5rem 1rem', borderRadius: '6px', fontSize: '0.8rem' }}>
                Clear
              </button>
            </>
          )}
        </div>
      </div>

      {requests.length === 0 ? (
        <div className="empty-state">
          <span style={{ fontSize: '3rem' }}>📭</span>
          <p>No requests submitted yet. Go to "New Request" to create one.</p>
        </div>
      ) : (
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Employee</th>
                <th>Item</th>
                <th>Qty</th>
                <th>Unit Price</th>
                <th>Total</th>
                <th>Vendor</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((req, idx) => (
                <tr key={req.thread_id || idx}>
                  <td style={{ fontSize: '0.8rem' }}>{new Date(req.submitted_at).toLocaleString()}</td>
                  <td>{req.employee}</td>
                  <td>{req.item}</td>
                  <td>{req.quantity}</td>
                  <td>${req.price?.toFixed(2)}</td>
                  <td>${(req.quantity * req.price).toFixed(2)}</td>
                  <td>{req.vendor || '—'}</td>
                  <td>
                    <span className={`badge ${getStatusBadge(req.status)}`}>
                      {req.status || 'pending'}
                    </span>
                  </td>
                  <td>
                    {req.thread_id && (
                      <button
                        onClick={() => checkStatus(req.thread_id, idx)}
                        disabled={checking === idx}
                        style={{ background: '#7c83ff', color: '#fff', padding: '0.3rem 0.6rem', borderRadius: '4px', fontSize: '0.75rem' }}
                      >
                        {checking === idx ? '...' : '↻'}
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Show details for items with comments/notifications */}
      {requests.filter(r => r.comments || r.notification).length > 0 && (
        <div style={{ marginTop: '2rem' }}>
          <h2 style={{ fontSize: '1.1rem', marginBottom: '1rem', color: '#333' }}>Details</h2>
          {requests.filter(r => r.comments || r.notification).map((req, idx) => (
            <div key={idx} className="result-panel" style={{ marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '0.9rem' }}>
                {req.item} — <span className={`badge ${getStatusBadge(req.status)}`}>{req.status}</span>
              </h3>
              {req.notification && <p style={{ marginTop: '0.5rem', fontSize: '0.85rem' }}>{req.notification}</p>}
              {req.comments && !req.notification && <p style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: '#555' }}>{req.comments}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
