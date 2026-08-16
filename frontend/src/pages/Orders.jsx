import { useState, useEffect } from 'react'
import api from '../api'
import './Pages.css'

export default function Orders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getOrders()
      .then(data => setOrders(Array.isArray(data) ? data : []))
      .catch(() => setOrders([]))
      .finally(() => setLoading(false))
  }, [])

  const getStatusBadge = (status) => {
    const map = {
      pending: 'badge-pending',
      approved: 'badge-approved',
      ordered: 'badge-ordered',
      rejected: 'badge-rejected',
    }
    return map[status] || 'badge-pending'
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div className="page">
      <h1 className="page-title">Purchase Orders</h1>
      <p className="page-subtitle">All finalized purchase orders with full details</p>

      {orders.length === 0 ? (
        <div className="empty-state">
          <span style={{ fontSize: '3rem' }}>📋</span>
          <p>No purchase orders yet. Orders appear here after a request is fully approved and processed.</p>
        </div>
      ) : (
        <>
          {/* Summary cards */}
          <div className="card-grid" style={{ marginBottom: '2rem' }}>
            <div className="dash-card">
              <span className="dash-card-icon">📦</span>
              <h3>{orders.length}</h3>
              <p>Total Orders</p>
            </div>
            <div className="dash-card">
              <span className="dash-card-icon">💰</span>
              <h3>${orders.reduce((sum, o) => sum + (o.item_cost || 0), 0).toLocaleString()}</h3>
              <p>Total Spend</p>
            </div>
            <div className="dash-card">
              <span className="dash-card-icon">✅</span>
              <h3>{orders.filter(o => o.status === 'ordered' || o.status === 'approved').length}</h3>
              <p>Completed</p>
            </div>
            <div className="dash-card">
              <span className="dash-card-icon">❌</span>
              <h3>{orders.filter(o => o.status === 'rejected').length}</h3>
              <p>Rejected</p>
            </div>
          </div>

          {/* Orders table */}
          <div className="data-table">
            <table>
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>Item</th>
                  <th>Quantity</th>
                  <th>Total Cost</th>
                  <th>Vendor</th>
                  <th>Status</th>
                  <th>Employee ID</th>
                  <th>Department ID</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id}>
                    <td><strong>#{order.id}</strong></td>
                    <td>{order.item_name}</td>
                    <td>{order.item_quantity}</td>
                    <td>${order.item_cost?.toFixed(2)}</td>
                    <td>{order.vendor_name || '—'}</td>
                    <td>
                      <span className={`badge ${getStatusBadge(order.status)}`}>
                        {order.status || 'pending'}
                      </span>
                    </td>
                    <td>{order.employee_id || '—'}</td>
                    <td>{order.department_id || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}
