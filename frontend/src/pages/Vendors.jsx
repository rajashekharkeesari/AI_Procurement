import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function Vendors() {
  const [vendors, setVendors] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', contact_info: '', stationary_id: '', price: '' })
  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({ name: '', contact_info: '', stationary_id: '', price: '' })
  const [error, setError] = useState('')

  const fetchData = () => {
    api.getVendors()
      .then(data => setVendors(Array.isArray(data) ? data : []))
      .catch(() => setVendors([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      await api.createVendor({ name: form.name, contact_info: form.contact_info, stationary_id: parseInt(form.stationary_id), price: form.price ? parseFloat(form.price) : null })
      setForm({ name: '', contact_info: '', stationary_id: '', price: '' })
      setShowForm(false)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  const startEdit = (v) => {
    setEditingId(v.id)
    setEditForm({ name: v.name, contact_info: v.contact_info, stationary_id: v.stationary_id, price: v.price || '' })
  }

  const saveEdit = async (id) => {
    try {
      await api.updateVendor(id, { name: editForm.name, contact_info: editForm.contact_info, stationary_id: parseInt(editForm.stationary_id), price: editForm.price ? parseFloat(editForm.price) : null })
      setEditingId(null)
      fetchData()
    } catch (err) { setError(err.message) }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h1 className="page-title">Vendors</h1>
          <p className="page-subtitle" style={{ marginBottom: 0 }}>Registered vendor list</p>
        </div>
        <button className="submit-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Vendor'}
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
              <label>Contact Info</label>
              <input value={form.contact_info} onChange={(e) => setForm({ ...form, contact_info: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Stationary Item ID</label>
              <input type="number" value={form.stationary_id} onChange={(e) => setForm({ ...form, stationary_id: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Price ($)</label>
              <input type="number" step="0.01" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} placeholder="Vendor price for this item" />
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
              <th>Contact</th>
              <th>Item ID</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {vendors.map((v) => (
              <tr key={v.id}>
                <td>{v.id}</td>
                <td>
                  {editingId === v.id
                    ? <input value={editForm.name} onChange={(e) => setEditForm({ ...editForm, name: e.target.value })} style={{ padding: '0.3rem', width: '100%' }} />
                    : v.name}
                </td>
                <td>
                  {editingId === v.id
                    ? <input value={editForm.contact_info} onChange={(e) => setEditForm({ ...editForm, contact_info: e.target.value })} style={{ padding: '0.3rem', width: '100%' }} />
                    : v.contact_info}
                </td>
                <td>
                  {editingId === v.id
                    ? <input type="number" value={editForm.stationary_id} onChange={(e) => setEditForm({ ...editForm, stationary_id: e.target.value })} style={{ padding: '0.3rem', width: '60px' }} />
                    : v.stationary_id}
                </td>
                <td>
                  {editingId === v.id
                    ? <input type="number" step="0.01" value={editForm.price} onChange={(e) => setEditForm({ ...editForm, price: e.target.value })} style={{ padding: '0.3rem', width: '80px' }} />
                    : v.price ? `$${v.price.toFixed(2)}` : '—'}
                </td>
                <td>
                  {editingId === v.id ? (
                    <div style={{ display: 'flex', gap: '0.3rem' }}>
                      <button onClick={() => saveEdit(v.id)} style={{ background: '#27ae60', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Save</button>
                      <button onClick={() => setEditingId(null)} style={{ background: '#666', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Cancel</button>
                    </div>
                  ) : (
                    <button onClick={() => startEdit(v)} style={{ background: '#7c83ff', color: '#fff', padding: '0.3rem 0.5rem', borderRadius: '4px', fontSize: '0.75rem' }}>Edit</button>
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
