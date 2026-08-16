import { Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Layout from './components/Layout.jsx'
import ProcurementRequest from './pages/ProcurementRequest.jsx'
import ApprovalPage from './pages/ApprovalPage.jsx'
import WorkflowStatus from './pages/WorkflowStatus.jsx'
import Employees from './pages/Employees.jsx'
import Departments from './pages/Departments.jsx'
import Vendors from './pages/Vendors.jsx'
import Stationary from './pages/Stationary.jsx'
import Orders from './pages/Orders.jsx'
import MyRequests from './pages/MyRequests.jsx'
import './App.css'

function App() {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user')
    return saved ? JSON.parse(saved) : null
  })

  useEffect(() => {
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  }, [user])

  const logout = () => {
    setUser(null)
    localStorage.removeItem('user')
  }

  if (!user) {
    return (
      <Routes>
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/signup" element={<Signup setUser={setUser} />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    )
  }

  return (
    <Layout user={user} logout={logout}>
      <Routes>
        <Route path="/" element={<Dashboard user={user} />} />
        <Route path="/procurement" element={<ProcurementRequest user={user} />} />
        {(user.role === 'admin' || user.role === 'manager') && (
          <Route path="/approval" element={<ApprovalPage user={user} />} />
        )}
        <Route path="/status" element={<WorkflowStatus />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/departments" element={<Departments />} />
        <Route path="/vendors" element={<Vendors />} />
        <Route path="/stationary" element={<Stationary />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/my-requests" element={<MyRequests />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Layout>
  )
}

export default App
