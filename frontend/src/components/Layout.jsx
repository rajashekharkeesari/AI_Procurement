import { NavLink } from 'react-router-dom'
import './Layout.css'

const navItems = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/procurement', label: 'New Request', icon: '📝' },
  { to: '/my-requests', label: 'My Requests', icon: '📜' },
  { to: '/approval', label: 'Approvals', icon: '✅', adminOnly: true },
  { to: '/orders', label: 'Orders', icon: '📋' },
  { to: '/status', label: 'Workflow Status', icon: '🔄' },
  { to: '/employees', label: 'Employees', icon: '👥' },
  { to: '/departments', label: 'Departments', icon: '🏢' },
  { to: '/vendors', label: 'Vendors', icon: '🏪' },
  { to: '/stationary', label: 'Stationary', icon: '📦' },
]

export default function Layout({ user, logout, children }) {
  const isAdmin = user.role === 'admin' || user.role === 'manager'
  const visibleItems = navItems.filter(item => !item.adminOnly || isAdmin)
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>AI Procurement</h2>
          <span className="user-badge">{user.username} ({user.role})</span>
        </div>

        <nav className="sidebar-nav">
          {visibleItems.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <span className="nav-icon">{icon}</span>
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <button className="logout-btn" onClick={logout}>
          Logout
        </button>
      </aside>

      <main className="main-content">{children}</main>
    </div>
  )
}
