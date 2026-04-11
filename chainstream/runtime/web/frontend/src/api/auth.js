/**
 * Authentication API functions
 */

const API_BASE_URL = 'http://localhost:6677/api'

/**
 * Login user
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} Login response
 */
export async function login(username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password
    })
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Login failed')
  }
  
  return data
}

/**
 * Register new user
 * @param {string} username - Username
 * @param {string} password - Password
 * @param {number} level - User level
 * @returns {Promise<Object>} Registration response
 */
export async function register(username, password, level = 1) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username,
      password,
      level
    })
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Registration failed')
  }
  
  return data
}

/**
 * Get current user info
 * @returns {Promise<Object>} User info
 */
export async function getCurrentUser() {
  const token = localStorage.getItem('token')
  
  if (!token) {
    throw new Error('No token found')
  }
  
  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Failed to get user info')
  }
  
  return data
}

/**
 * Change user password
 * @param {string} oldPassword - Current password
 * @param {string} newPassword - New password
 * @returns {Promise<Object>} Change password response
 */
export async function changePassword(oldPassword, newPassword) {
  const token = localStorage.getItem('token')
  
  if (!token) {
    throw new Error('No token found')
  }
  
  const response = await fetch(`${API_BASE_URL}/auth/change-password`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword
    })
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Failed to change password')
  }
  
  return data
}

/**
 * Enable encryption for user
 * @param {string} password - Optional password for key derivation
 * @returns {Promise<Object>} Enable encryption response
 */
export async function enableEncryption(password = null) {
  const token = localStorage.getItem('token')
  
  if (!token) {
    throw new Error('No token found')
  }
  
  const response = await fetch(`${API_BASE_URL}/auth/enable-encryption`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      password
    })
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Failed to enable encryption')
  }
  
  return data
}

/**
 * Disable encryption for user
 * @returns {Promise<Object>} Disable encryption response
 */
export async function disableEncryption() {
  const token = localStorage.getItem('token')
  
  if (!token) {
    throw new Error('No token found')
  }
  
  const response = await fetch(`${API_BASE_URL}/auth/disable-encryption`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.message || 'Failed to disable encryption')
  }
  
  return data
}

/**
 * Logout user (clear local storage)
 */
export function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if authenticated
 */
export function isAuthenticated() {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')
  return !!(token && user)
}

/**
 * Get stored user info
 * @returns {Object|null} User info or null
 */
export function getStoredUser() {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch (e) {
      return null
    }
  }
  return null
}

/**
 * Get stored token
 * @returns {string|null} Token or null
 */
export function getStoredToken() {
  return localStorage.getItem('token')
}
