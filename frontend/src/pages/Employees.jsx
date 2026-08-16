import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function Employees() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', department_id: '' })
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({ name: '', department_id: '' })
  const [error, setError] = useState('')

  const fetchData = () => {
    api.getEmployees()
      .then(data => setEmployees(Array.isArray(data) ? data : []))
      .catch(() => setEmployees([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.createEmployee({ name: form.name, department_id: parseInt(form.department_id) })
      setForm({ name: '', department_id: '' })
      setShowForm(false)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  const startEdit = (emp) => {
    setEditingId(emp.id)
    setEditForm({ name: emp.name, department_id: emp.department_id })
  }

  const saveEdit = async (id) => {
    try {
      await api.updateEmployee(id, { name: editForm.name, department_id: parseInt(editForm.department_id) })
      setEditingId(null)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 className="page-title">Employees</h1>
          <p className="page-subtitle" style={{ marginBottom: 0 }}>All employees in the system</p>
        </div>
        <button className="submit-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Employee'}
        </button>
      </div>

      {error && <div className="auth-error" style={{ marginBottom: '1rem' }}>{error}</div>}

      {showForm && (
        <div className="form-card" style={{ marginBottom: '1.5rem' }}>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name</label>
              <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Department ID</label>
              <input type="number" value={form.department_id} onChange={(e) => setForm({ ...form, department_id: e.target.value })} required />
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
              <th>Department ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td>{emp.id}</td>
                <td>
                  {editingId === emp.id
                    ? <input value={editForm.name} onChange={(e) => setEditForm({ ...editForm, name: e.target.value })} style={{ padding: '0.3rem', width: '100%' }} />
                    : emp.name}
                </td>
                <td>
                  {editingId === emp.id
                    ? <input type="number" value={editForm.department_id} onChange={(e) => setEditForm({ ...editForm, department_id: e.target.value })} style={{ padding: '0.3rem', width: '60px' }} />
                    : emp.department_id}
                </td>
                <td>
                  {editingId === emp.id ? (
                    <div style={{ display: 'flex', gap: '0.3rem' }}>
                      <button onClick={() => saveEdit(emp.id)} style={{ background: '#27ae60', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Save</button>
                      <button onClick={() => setEditingId(null)} style={{ background: '#666', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Cancel</button>
                    </div>
                  ) : (
                    <button onClick={() => startEdit(emp)} style={{ background: '#7c83ff', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Edit</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
