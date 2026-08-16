import { Link } from 'react-router-dom'
import './Pages.css'

export default function Dashboard({ user }) {
  return (
    <div className="page">
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">Welcome back, {user.username}</p>

      <div className="card-grid">
        <Link to="/procurement" className="dash-card">
          <span className="dash-card-icon">📝</span>
          <h3>New Request</h3>
          <p>Submit a procurement request</p>
        </Link>

        <Link to="/approval" className="dash-card">
          <span className="dash-card-icon">✅</span>
          <h3>Approvals</h3>
          <p>Review pending requests</p>
        </Link>

        <Link to="/status" className="dash-card">
          <span className="dash-card-icon">🔄</span>
          <h3>Workflow Status</h3>
          <p>Track your requests</p>
        </Link>

        <Link to="/employees" className="dash-card">
          <span className="dash-card-icon">👥</span>
          <h3>Employees</h3>
          <p>View all employees</p>
        </Link>

        <Link to="/departments" className="dash-card">
          <span className="dash-card-icon">🏢</span>
          <h3>Departments</h3>
          <p>Department budgets and limits</p>
        </Link>

        <Link to="/vendors" className="dash-card">
          <span className="dash-card-icon">🏪</span>
          <h3>Vendors</h3>
          <p>Manage vendor list</p>
        </Link>

        <Link to="/stationary" className="dash-card">
          <span className="dash-card-icon">📦</span>
          <h3>Stationary</h3>
          <p>Items catalogue</p>
        </Link>
      </div>
    </div>
  )
}
