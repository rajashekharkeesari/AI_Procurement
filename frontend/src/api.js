// API client for the AI Procurement backend.
// Base URL is read from the VITE_API_BASE_URL environment variable.

const BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  let data
  const text = await res.text()
  try {
    data = text ? JSON.parse(text) : {}
  } catch {
    data = { detail: text }
  }

  if (!res.ok) {
    throw new Error(data.detail || `Request failed (${res.status})`)
  }
  return data
}

export const api = {
  // --- Auth ---
  register: (payload) =>
    request('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),

  login: (payload) =>
    request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),

  // --- Workflow ---
  runWorkflow: (payload) =>
    request('/workflow/run', { method: 'POST', body: JSON.stringify(payload) }),

  resumeWorkflow: (payload) =>
    request('/workflow/resume', { method: 'POST', body: JSON.stringify(payload) }),

  workflowStatus: (threadId) => request(`/workflow/status/${threadId}`),

  // --- Data ---
  getEmployees: () => request('/employees'),
  getDepartments: () => request('/departments'),
  getVendors: () => request('/vendors'),
  getStationary: () => request('/stationary'),
  getOrders: () => request('/orders'),

  // --- Create ---
  createEmployee: (payload) =>
    request('/employees', { method: 'POST', body: JSON.stringify(payload) }),
  createDepartment: (payload) =>
    request('/departments', { method: 'POST', body: JSON.stringify(payload) }),
  createVendor: (payload) =>
    request('/vendors', { method: 'POST', body: JSON.stringify(payload) }),
  createStationary: (payload) =>
    request('/stationary', { method: 'POST', body: JSON.stringify(payload) }),

  // --- Requests history ---
  getRequests: () => request('/requests'),

  // --- Update ---
  updateEmployee: (id, payload) =>
    request(`/employees/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  updateDepartment: (id, payload) =>
    request(`/departments/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  updateVendor: (id, payload) =>
    request(`/vendors/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  updateStationary: (id, payload) =>
    request(`/stationary/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
}

export default api
