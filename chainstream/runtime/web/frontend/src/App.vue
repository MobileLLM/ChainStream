<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Header from './components/header.vue'
import Aside from './components/aside.vue'
import Login from './components/Login.vue'
import { isAuthenticated, getStoredUser } from './api/auth.js'

const router = useRouter()
const isLoggedIn = ref(false)
const currentUser = ref(null)
const screenWidth = ref(window.innerWidth)
const isCollapsed = ref(false)

// 响应式计算侧边栏宽度
const asideWidth = computed(() => {
  if (screenWidth.value < 768) {
    return isCollapsed.value ? '0px' : '280px'
  } else if (screenWidth.value < 1024) {
    return isCollapsed.value ? '0px' : '260px'
  } else {
    return isCollapsed.value ? '0px' : '300px'
  }
})

// 监听窗口大小变化
const handleResize = () => {
  screenWidth.value = window.innerWidth
  // 在小屏幕上自动折叠侧边栏
  if (screenWidth.value < 768 && !isCollapsed.value) {
    isCollapsed.value = true
  }
}

onMounted(() => {
  checkAuthStatus()
  window.addEventListener('resize', handleResize)
  handleResize() // 初始化时调用一次
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const checkAuthStatus = () => {
  if (isAuthenticated()) {
    isLoggedIn.value = true
    currentUser.value = getStoredUser()
  } else {
    isLoggedIn.value = false
    currentUser.value = null
  }
}

const handleLoginSuccess = (user) => {
  isLoggedIn.value = true
  currentUser.value = user
  router.push('/')
}

const handleLogout = () => {
  isLoggedIn.value = false
  currentUser.value = null
  router.push('/login')
}

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}
</script>

<template>
  <div v-if="!isLoggedIn">
    <Login @login-success="handleLoginSuccess" />
  </div>
  
  <el-container v-else class="app-container">
    <el-header class="app-header">
      <Header :user="currentUser" @logout="handleLogout" @toggle-sidebar="toggleSidebar" />
    </el-header>

    <el-container class="main-container">
      <el-aside class="app-aside" :width="asideWidth">
        <Aside :user="currentUser" />
      </el-aside>
      <el-main class="app-main">
        <router-view :user="currentUser"></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>


</script>

<style scoped>
.app-container {
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.app-header {
  padding: 0;
  margin: 0;
  border: none;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.main-container {
  height: calc(100vh - 60px);
  width: 100%;
  margin: 0;
  padding: 0;
}

.app-aside {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  transition: width 0.3s ease;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.app-main {
  background-color: #f5f7fa;
  padding: 0;
  margin: 0;
  overflow: auto;
  transition: margin-left 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .app-aside {
    position: absolute;
    z-index: 999;
    height: 100%;
  }
  
  .app-main {
    margin-left: 0;
  }
}

@media (max-width: 768px) {
  .app-header {
    height: 50px;
  }
  
  .main-container {
    height: calc(100vh - 50px);
  }
  
  .app-aside {
    width: 280px !important;
  }
}

@media (max-width: 480px) {
  .app-aside {
    width: 100% !important;
  }
}

/* 全局样式重置 */
:deep(.el-container),
:deep(.el-header),
:deep(.el-aside),
:deep(.el-main) {
  padding: 0;
  margin: 0;
}

:deep(.el-container) {
  width: 100%;
  height: 100%;
}

:deep(.el-aside) {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

