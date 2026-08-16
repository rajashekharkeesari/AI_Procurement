import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

const STORAGE_KEY = 'procurement_form'
const RESULT_KEY = 'procurement_result'

export default function ProcurementRequest({ user }) {
  const [form, setForm] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : {
      employee: user.username,
      item: '',
      quantity: 1,
      price: 0,
      vendor: '',
    }
  })
  const [result, setResult] = useState(() => {
    const saved = localStorage.getItem(RESULT_KEY)
    return saved ? JSON.parse(saved) : null
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Persist form on change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(form))
  }, [form])

  // Persist result on change
  useEffect(() => {
    if (result) {
      localStorage.setItem(RESULT_KEY, JSON.stringify(result))
    } else {
      localStorage.removeItem(RESULT_KEY)
    }
  }, [result])

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: name === 'quantity' || name === 'price' ? Number(value) : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setResult(null)
    setLoading(true)

    try {
      const data = await api.runWorkflow(form)
      setResult(data)

      // Save thread_id if workflow is paused
      if (!data.completed && data.thread_id) {
        const pending = JSON.parse(localStorage.getItem('pending_approvals') || '[]')
        pending.push({
          thread_id: data.thread_id,
          employee: form.employee,
          item: form.item,
          total_cost: form.quantity * form.price,
          summary: data.approval_summary,
          created_at: new Date().toISOString(),
        })
        localStorage.setItem('pending_approvals', JSON.stringify(pending))
      }

      // Track in my_requests history
      const history = JSON.parse(localStorage.getItem('my_requests') || '[]')
      history.unshift({
        thread_id: data.thread_id,
        employee: form.employee,
        item: form.item,
        quantity: form.quantity,
        price: form.price,
        vendor: form.vendor,
        status: data.completed
          ? (data.workflow_state?.status || 'completed')
          : 'awaiting_approval',
        submitted_at: new Date().toISOString(),
      })
      localStorage.setItem('my_requests', JSON.stringify(history))
    } catch (err) {
      setError(err.message || 'Failed to submit request')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setForm({ employee: user.username, item: '', quantity: 1, price: 0, vendor: '' })
    setResult(null)
    setError('')
  }

  return (
    <div className="page">
      <h1 className="page-title">New Procurement Request</h1>
      <p className="page-subtitle">Submit a new procurement request through the AI workflow</p>

      <div className="form-card">
        <form onSubmit={handleSubmit}>
          {error && <div className="auth-error">{error}</div>}

          <div className="form-group">
            <label htmlFor="employee">Employee</label>
            <input
              id="employee"
              name="employee"
              value={form.employee}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="item">Item</label>
            <input
              id="item"
              name="item"
              value={form.item}
              onChange={handleChange}
              placeholder="e.g. Printer Toner Cartridge"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="quantity">Quantity</label>
            <input
              id="quantity"
              name="quantity"
              type="number"
              min="1"
              value={form.quantity}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="price">Unit Price ($)</label>
            <input
              id="price"
              name="price"
              type="number"
              min="0"
              step="0.01"
              value={form.price}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="vendor">Preferred Vendor (optional)</label>
            <input
              id="vendor"
              name="vendor"
              value={form.vendor}
              onChange={handleChange}
              placeholder="e.g. Office Depot"
            />
          </div>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Processing...' : 'Submit Request'}
            </button>
            <button type="button" className="submit-btn" onClick={handleClear} style={{ background: '#666' }}>
              Clear
            </button>
          </div>
        </form>
      </div>

      {result && (
        <div className="result-panel">
          <h3>
            {result.completed ? '✅ Workflow Complete' : '⏸️ Awaiting Approval'}
          </h3>
          {!result.completed && (
            <p style={{ marginBottom: '1rem', color: '#856404' }}>
              Request is waiting for human approval. Thread ID: <code>{result.thread_id}</code>
            </p>
          )}
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
