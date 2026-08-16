import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function Departments() {
  const [departments, setDepartments] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', budget: '', policy_limit: '' })
  const [error, setError] = useState('')

  const fetchData = () => {
    api.getDepartments()
      .then(data => setDepartments(Array.isArray(data) ? data : []))
      .catch(() => setDepartments([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.createDepartment({
        name: form.name,
        budget: parseFloat(form.budget),
        policy_limit: parseFloat(form.policy_limit),
      })
      setForm({ name: '', budget: '', policy_limit: '' })
      setShowForm(false)
      fetchData()
    } catch (err) {
      setError(err.message)
    }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 className="page-title">Departments</h1>
          <p className="page-subtitle" style={{ marginBottom: 0 }}>Department budgets and policy limits</p>
        </div>
        <button className="submit-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Department'}
        </button>
      </div>

      {showForm && (
        <div className="form-card" style={{ marginBottom: '1.5rem' }}>
          <form onSubmit={handleSubmit}>
            {error && <div className="auth-error">{error}</div>}
            <div className="form-group">
              <label>Name</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Budget ($)</label>
              <input type="number" step="0.01" value={form.budget} onChange={(e) => setForm({ ...form, budget: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Policy Limit ($)</label>
              <input type="number" step="0.01" value={form.policy_limit} onChange={(e) => setForm({ ...form, policy_limit: e.target.value })} required />
            </div>
            <button type="submit" className="submit-btn">Save</button>
          </form>
        </div>
      )}

      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Budget</th>
              <th>Policy Limit</th>
            </tr>
          </thead>
          <tbody>
            {departments.map((dept) => (
              <tr key={dept.id}>
                <td>{dept.id}</td>
                <td>{dept.name}</td>
                <td>${dept.budget?.toLocaleString()}</td>
                <td>${dept.policy_limit?.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
