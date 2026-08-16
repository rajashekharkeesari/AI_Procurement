import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function Stationary() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', cost: '', quantity: '' })
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({ name: '', cost: '', quantity: '' })
  const [error, setError] = useState('')

  const fetchData = () => {
    api.getStationary()
      .then(data => setItems(Array.isArray(data) ? data : []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.createStationary({ name: form.name, cost: parseFloat(form.cost), quantity: parseInt(form.quantity) })
      setForm({ name: '', cost: '', quantity: '' })
      setShowForm(false)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  const startEdit = (item) => {
    setEditingId(item.id)
    setEditForm({ name: item.name, cost: item.cost, quantity: item.quantity })
  }

  const saveEdit = async (id) => {
    try {
      await api.updateStationary(id, { name: editForm.name, cost: parseFloat(editForm.cost), quantity: parseInt(editForm.quantity) })
      setEditingId(null)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 className="page-title">Stationary Items</h1>
          <p className="page-subtitle" style={{ marginBottom: 0 }}>Available items catalogue (stock deducted on approved orders)</p>
        </div>
        <button className="submit-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Item'}
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
              <label>Unit Cost ($)</label>
              <input type="number" step="0.01" value={form.cost} onChange={(e) => setForm({ ...form, cost: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Quantity in Stock</label>
              <input type="number" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
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
              <th>Unit Cost</th>
              <th>In Stock</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>
                  {editingId === item.id
                    ? <input value={editForm.name} onChange={(e) => setEditForm({ ...editForm, name: e.target.value })} style={{ padding: '0.3rem', width: '100%' }} />
                    : item.name}
                </td>
                <td>
                  {editingId === item.id
                    ? <input type="number" step="0.01" value={editForm.cost} onChange={(e) => setEditForm({ ...editForm, cost: e.target.value })} style={{ padding: '0.3rem', width: '80px' }} />
                    : `$${item.cost?.toFixed(2)}`}
                </td>
                <td>
                  {editingId === item.id
                    ? <input type="number" value={editForm.quantity} onChange={(e) => setEditForm({ ...editForm, quantity: e.target.value })} style={{ padding: '0.3rem', width: '60px' }} />
                    : item.quantity}
                </td>
                <td>
                  {editingId === item.id ? (
                    <div style={{ display: 'flex', gap: '0.3rem' }}>
                      <button onClick={() => saveEdit(item.id)} style={{ background: '#27ae60', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Save</button>
                      <button onClick={() => setEditingId(null)} style={{ background: '#666', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Cancel</button>
                    </div>
                  ) : (
                    <button onClick={() => startEdit(item)} style={{ background: '#7c83ff', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Edit</button>
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
