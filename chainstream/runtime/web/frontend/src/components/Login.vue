<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">ChainStream Login</h2>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username:</label>
          <input
            id="username"
            v-model="loginForm.username"
            type="text"
            required
            placeholder="Enter your username"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password:</label>
          <input
            id="password"
            v-model="loginForm.password"
            type="password"
            required
            placeholder="Enter your password"
            class="form-input"
          />
        </div>
        
        <button type="submit" :disabled="loading" class="login-button">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div class="register-link">
        <p>Don't have an account? <a href="#" @click.prevent="showRegister = true">Register here</a></p>
      </div>
    </div>
    
    <!-- Registration Modal -->
    <div v-if="showRegister" class="modal-overlay" @click="showRegister = false">
      <div class="modal-content" @click.stop>
        <h3>Register New User</h3>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="reg-username">Username:</label>
            <input
              id="reg-username"
              v-model="registerForm.username"
              type="text"
              required
              placeholder="Enter username"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="reg-password">Password:</label>
            <input
              id="reg-password"
              v-model="registerForm.password"
              type="password"
              required
              placeholder="Enter password"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="reg-level">User Level:</label>
            <select id="reg-level" v-model="registerForm.level" class="form-input">
              <option value="1">Level 1 (Basic User)</option>
              <option value="5">Level 5 (Advanced User)</option>
              <option value="10">Level 10 (Admin)</option>
            </select>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showRegister = false" class="cancel-button">
              Cancel
            </button>
            <button type="submit" :disabled="registerLoading" class="register-button">
              {{ registerLoading ? 'Creating...' : 'Create Account' }}
            </button>
          </div>
        </form>
        
        <div v-if="registerError" class="error-message">
          {{ registerError }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { login, register } from '../api/auth.js'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        level: 1
      },
      loading: false,
      registerLoading: false,
      error: '',
      registerError: '',
      showRegister: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      
      try {
        const response = await login(this.loginForm.username, this.loginForm.password)
        
        if (response.success) {
          // Store token and user info
          localStorage.setItem('token', response.token)
          localStorage.setItem('user', JSON.stringify(response.user))
          
          // Emit login event to parent
          this.$emit('login-success', response.user)
          
          // Redirect to home or emit event to parent component
          this.$router.push('/')
        } else {
          this.error = response.message || 'Login failed'
        }
      } catch (error) {
        this.error = 'Network error. Please try again.'
        console.error('Login error:', error)
      } finally {
        this.loading = false
      }
    },
    
    async handleRegister() {
      this.registerLoading = true
      this.registerError = ''
      
      try {
        const response = await register(
          this.registerForm.username, 
          this.registerForm.password, 
          parseInt(this.registerForm.level)
        )
        
        if (response.success) {
          this.showRegister = false
          this.registerForm = { username: '', password: '', level: 1 }
          alert('Account created successfully! Please login.')
        } else {
          this.registerError = response.message || 'Registration failed'
        }
      } catch (error) {
        this.registerError = 'Network error. Please try again.'
        console.error('Registration error:', error)
      } finally {
        this.registerLoading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 28px;
  font-weight: 600;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  border: 1px solid #fcc;
}

.register-link {
  text-align: center;
}

.register-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  text-decoration: underline;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h3 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

.register-form {
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.cancel-button {
  flex: 1;
  padding: 12px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.register-button {
  flex: 1;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
}

.cancel-button:hover,
.register-button:hover:not(:disabled) {
  opacity: 0.9;
}

.register-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
