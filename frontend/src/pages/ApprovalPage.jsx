import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function ApprovalPage({ user }) {
  const [pendingApprovals, setPendingApprovals] = useState([])
  const [completedApprovals, setCompletedApprovals] = useState([])
  const [comments, setComments] = useState({})
  const [processing, setProcessing] = useState(null)

  useEffect(() => {
    const pending = JSON.parse(localStorage.getItem('pending_approvals') || '[]')
    const completed = JSON.parse(localStorage.getItem('completed_approvals') || '[]')
    setPendingApprovals(pending)
    setCompletedApprovals(completed)
  }, [])

  const handleDecision = async (threadId, approved) => {
    setProcessing(threadId)

    try {
      const data = await api.resumeWorkflow({
        thread_id: threadId,
        approved,
        comment: comments[threadId] || (approved ? 'Approved' : 'Rejected'),
      })

      // Move from pending to completed
      const item = pendingApprovals.find((a) => a.thread_id === threadId)
      const completedItem = {
        ...item,
        decision: approved ? 'approved' : 'rejected',
        decided_at: new Date().toISOString(),
        reviewer_comment: comments[threadId] || '',
        result: data.workflow_state || {},
      }

      const updatedPending = pendingApprovals.filter((a) => a.thread_id !== threadId)
      const updatedCompleted = [completedItem, ...completedApprovals]

      setPendingApprovals(updatedPending)
      setCompletedApprovals(updatedCompleted)
      localStorage.setItem('pending_approvals', JSON.stringify(updatedPending))
      localStorage.setItem('completed_approvals', JSON.stringify(updatedCompleted))

      // Also update my_requests status
      const myReqs = JSON.parse(localStorage.getItem('my_requests') || '[]')
      const reqIdx = myReqs.findIndex(r => r.thread_id === threadId)
      if (reqIdx !== -1) {
        myReqs[reqIdx].status = approved ? 'approved' : 'rejected'
        localStorage.setItem('my_requests', JSON.stringify(myReqs))
      }
    } catch (err) {
      alert('Error: ' + err.message)
    } finally {
      setProcessing(null)
    }
  }

  const clearCompleted = () => {
    setCompletedApprovals([])
    localStorage.removeItem('completed_approvals')
  }

  return (
    <div className="page">
      <h1 className="page-title">Approvals</h1>
      <p className="page-subtitle">Pending requests and past decisions</p>

      {/* Pending Section */}
      <h2 style={{ fontSize: '1.1rem', margin: '1.5rem 0 1rem', color: '#333' }}>
        Pending ({pendingApprovals.length})
      </h2>

      {pendingApprovals.length === 0 ? (
        <div className="empty-state" style={{ padding: '2rem' }}>
          <p>No pending approvals</p>
        </div>
      ) : (
        pendingApprovals.map((item) => (
          <div key={item.thread_id} className="form-card" style={{ marginBottom: '1.5rem' }}>
            <h3 style={{ marginBottom: '1rem' }}>Request from {item.employee}</h3>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', marginBottom: '1rem' }}>
              <div><strong>Item:</strong> {item.item}</div>
              <div><strong>Total Cost:</strong> ${item.total_cost?.toFixed(2)}</div>
              <div><strong>Thread ID:</strong> <code style={{ fontSize: '0.7rem' }}>{item.thread_id}</code></div>
              <div><strong>Submitted:</strong> {new Date(item.created_at).toLocaleString()}</div>
            </div>

            {item.summary && (
              <div style={{ background: '#f8f9fa', padding: '1rem', borderRadius: '6px', marginBottom: '1rem' }}>
                <strong>AI Summary:</strong>
                <p style={{ marginTop: '0.5rem', fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>
                  {typeof item.summary === 'object' ? item.summary.summary || JSON.stringify(item.summary) : item.summary}
                </p>
              </div>
            )}

            <div className="form-group">
              <label>Comment (optional)</label>
              <input
                type="text"
                value={comments[item.thread_id] || ''}
                onChange={(e) => setComments({ ...comments, [item.thread_id]: e.target.value })}
                placeholder="Add a comment..."
              />
            </div>

            <div className="action-btns">
              <button
                className="btn-approve"
                onClick={() => handleDecision(item.thread_id, true)}
                disabled={processing === item.thread_id}
              >
                {processing === item.thread_id ? 'Processing...' : '✓ Approve'}
              </button>
              <button
                className="btn-reject"
                onClick={() => handleDecision(item.thread_id, false)}
                disabled={processing === item.thread_id}
              >
                ✗ Reject
              </button>
            </div>
          </div>
        ))
      )}

      {/* Completed Section */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', margin: '2rem 0 1rem' }}>
        <h2 style={{ fontSize: '1.1rem', color: '#333' }}>
          Past Decisions ({completedApprovals.length})
        </h2>
        {completedApprovals.length > 0 && (
          <button onClick={clearCompleted} style={{ background: 'none', color: '#666', fontSize: '0.8rem', padding: '0.3rem 0.6rem', border: '1px solid #ddd', borderRadius: '4px' }}>
            Clear
          </button>
        )}
      </div>

      {completedApprovals.length === 0 ? (
        <div className="empty-state" style={{ padding: '2rem' }}>
          <p>No past decisions</p>
        </div>
      ) : (
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Employee</th>
                <th>Item</th>
                <th>Cost</th>
                <th>Decision</th>
                <th>Comment</th>
              </tr>
            </thead>
            <tbody>
              {completedApprovals.map((item, idx) => (
                <tr key={idx}>
                  <td style={{ fontSize: '0.8rem' }}>{new Date(item.decided_at).toLocaleString()}</td>
                  <td>{item.employee}</td>
                  <td>{item.item}</td>
                  <td>${item.total_cost?.toFixed(2)}</td>
                  <td>
                    <span className={`badge ${item.decision === 'approved' ? 'badge-approved' : 'badge-rejected'}`}>
                      {item.decision}
                    </span>
                  </td>
                  <td style={{ fontSize: '0.8rem', color: '#666' }}>{item.reviewer_comment || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
