<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">{{ $t('login.title') }}</h2>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">{{ $t('login.username') }}:</label>
          <input
            id="username"
            v-model="loginForm.username"
            type="text"
            required
            :placeholder="$t('login.enterUsername')"
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <label for="password">{{ $t('login.password') }}:</label>
          <input
            id="password"
            v-model="loginForm.password"
            type="password"
            required
            :placeholder="$t('login.enterPassword')"
            class="form-input"
          />
        </div>
        
        <button type="submit" :disabled="loading" class="login-button">
          {{ loading ? $t('login.loggingIn') : $t('login.login') }}
        </button>
      </form>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div class="register-link">
        <p>{{ $t('login.noAccount') }} <a href="#" @click.prevent="showRegister = true">{{ $t('login.registerHere') }}</a></p>
      </div>
    </div>
    
    <!-- Registration Modal -->
    <div v-if="showRegister" class="modal-overlay" @click="showRegister = false">
      <div class="modal-content" @click.stop>
        <h3>{{ $t('login.registerTitle') }}</h3>
        
        <form @submit.prevent="handleRegister" class="register-form">
          <div class="form-group">
            <label for="reg-username">{{ $t('login.username') }}:</label>
            <input
              id="reg-username"
              v-model="registerForm.username"
              type="text"
              required
              :placeholder="$t('login.enterUsername')"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="reg-password">{{ $t('login.password') }}:</label>
            <input
              id="reg-password"
              v-model="registerForm.password"
              type="password"
              required
              :placeholder="$t('login.enterPassword')"
              class="form-input"
            />
          </div>
          
          <div class="form-group">
            <label for="reg-level">{{ $t('login.userLevel') }}:</label>
            <select id="reg-level" v-model="registerForm.level" class="form-input">
              <option value="1">{{ $t('login.level1') }}</option>
              <option value="5">{{ $t('login.level5') }}</option>
              <option value="10">{{ $t('login.level10') }}</option>
            </select>
          </div>
          
          <div class="form-actions">
            <button type="button" @click="showRegister = false" class="cancel-button">
              {{ $t('common.cancel') }}
            </button>
            <button type="submit" :disabled="registerLoading" class="register-button">
              {{ registerLoading ? $t('login.creating') : $t('login.createAccount') }}
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
import { useI18n } from 'vue-i18n'

export default {
  name: 'Login',
  setup() {
    const { t } = useI18n()
    return { t }
  },
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
          this.error = response.message || this.t('login.loginFailed')
        }
      } catch (error) {
        this.error = this.t('login.networkError')
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
          alert(this.t('login.registerSuccess'))
        } else {
          this.registerError = response.message || this.t('login.registerFailed')
        }
      } catch (error) {
        this.registerError = this.t('login.networkError')
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
