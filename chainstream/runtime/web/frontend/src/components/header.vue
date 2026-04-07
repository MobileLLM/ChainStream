<template>
  <div class="header-container">
    <div class="header-left">
      <el-button 
        class="sidebar-toggle" 
        @click="toggleSidebar"
        :icon="Fold"
        circle
        size="small"
      />
      <h1 class="logo">{{ $t('header.title') }}</h1>
    </div>
    
    <div class="header-right">
      <div class="language-switcher">
        <el-dropdown trigger="click" @command="handleLanguageChange">
          <el-button class="language-button" :icon="Operation" circle size="small" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="zh-CN" :class="{ 'is-active': currentLanguage === 'zh-CN' }">
                {{ $t('header.chinese') }}
              </el-dropdown-item>
              <el-dropdown-item command="en-US" :class="{ 'is-active': currentLanguage === 'en-US' }">
                {{ $t('header.english') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      
      <div v-if="user" class="user-info">
        <el-avatar 
          :size="32" 
          class="user-avatar"
        >
          {{ user.username?.charAt(0).toUpperCase() }}
        </el-avatar>
        <div class="user-details">
          <span class="username">{{ user.username }}</span>
          <el-tag size="small" type="info" class="user-level">{{ $t('header.level') }} {{ user.level }}</el-tag>
        </div>
        <el-dropdown trigger="click" class="user-menu">
          <el-button :icon="Setting" circle size="small" class="menu-button" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="showUserProfile">
                <el-icon><User /></el-icon>
                {{ $t('header.profile') }}
              </el-dropdown-item>
              <el-dropdown-item @click="showSettings">
                <el-icon><Setting /></el-icon>
                {{ $t('header.settings') }}
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                <el-icon><SwitchButton /></el-icon>
                {{ $t('header.logout') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
  background: transparent;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.sidebar-toggle {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.logo {
  color: white;
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.language-switcher {
  display: flex;
  align-items: center;
}

.language-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
  }
}

:deep(.el-dropdown-menu__item.is-active) {
  color: #409EFF;
  font-weight: 600;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.2);
  }
}

.user-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.username {
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  line-height: 1;
}

.user-level {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  font-size: 0.7rem;
  height: 18px;
  line-height: 16px;
}

.menu-button {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 12px;
  }
  
  .logo {
    font-size: 1.1rem;
  }
  
  .user-details {
    display: none;
  }
  
  .user-info {
    padding: 6px 12px;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0 8px;
  }
  
  .logo {
    font-size: 1rem;
  }
  
  .sidebar-toggle {
    display: none;
  }
}
</style>
<script setup>
import { defineProps, defineEmits, computed } from 'vue'
import { Fold, Setting, User, SwitchButton, Operation } from '@element-plus/icons-vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['logout', 'toggle-sidebar'])

const { locale } = useI18n()

const currentLanguage = computed(() => locale.value)

const handleLogout = () => {
  emit('logout')
}

const toggleSidebar = () => {
  emit('toggle-sidebar')
}

const showUserProfile = () => {
  // TODO: Implement user profile modal
  console.log('Show user profile')
}

const showSettings = () => {
  // TODO: Implement settings modal
  console.log('Show settings')
}

const handleLanguageChange = (lang) => {
  locale.value = lang
  localStorage.setItem('language', lang)
  // 刷新页面以确保所有组件都更新语言
  window.location.reload()
}
</script>