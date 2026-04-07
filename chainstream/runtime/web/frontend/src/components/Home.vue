<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  Setting, 
  CopyDocument, 
  Connection, 
  Refresh, 
  Monitor, 
  DataLine,
  SuccessFilled,
  CircleCloseFilled
} from '@element-plus/icons-vue'
</script>

<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1 class="welcome-title">{{ $t('home.welcome') }}</h1>
      <p class="welcome-subtitle">{{ $t('home.subtitle') }}</p>
    </div>

    <div class="config-section">
      <el-card class="config-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="header-icon"><Setting /></el-icon>
            <span class="card-title">{{ $t('home.systemConfiguration') }}</span>
          </div>
        </template>
        
        <div class="config-content" v-loading="loading">
          <el-descriptions
            :title="$t('home.backendConnection')"
            :column="responsiveColumns"
            size="default"
            border
            direction="vertical"
            class="connection-descriptions"
          >
            <el-descriptions-item :label="$t('home.backendUrl')" label-class-name="desc-label">
              <div class="url-display">
                <el-text class="url-text" type="primary">{{ backendUrl }}</el-text>
                <el-button 
                  size="small" 
                  :icon="CopyDocument"
                  @click="copyUrl"
                  circle
                  class="copy-btn"
                />
              </div>
            </el-descriptions-item>
            
            <el-descriptions-item :label="$t('home.connectionStatus')" label-class-name="desc-label">
              <div class="status-display">
                <el-tag 
                  :type="connectionStatus.type" 
                  :icon="connectionStatus.icon"
                  size="default"
                >
                  {{ connectionStatus.text }}
                </el-tag>
              </div>
            </el-descriptions-item>
            
            <el-descriptions-item :label="$t('common.actions')" label-class-name="desc-label">
              <div class="action-buttons">
                <el-button 
                  type="primary" 
                  :icon="Connection"
                  @click="checkConn()"
                  :loading="loading"
                  size="default"
                >
                  {{ $t('home.testConnection') }}
                </el-button>
                <el-button 
                  type="default" 
                  :icon="Refresh"
                  @click="refreshConfig"
                  size="default"
                >
                  {{ $t('common.refresh') }}
                </el-button>
              </div>
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-card>
    </div>

    <div class="stats-section">
      <el-row :gutter="16" class="stats-row">
        <el-col :xs="24" :sm="12" :md="12" class="stat-col">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><Monitor /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ runningAgentsCount }}</div>
                <div class="stat-label">{{ $t('home.runningAgents') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :xs="24" :sm="12" :md="12" class="stat-col">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon><DataLine /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ activeStreamsCount }}</div>
                <div class="stat-label">{{ $t('home.activeStreams') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue'
import { checkConnection } from '@/api/home.js'
import { getStatistics } from '@/api/monitor/statistics.js'
import axios from "axios";
import { useI18n } from 'vue-i18n'

export default {
  name: 'Home',
  setup() {
    const { t } = useI18n()
    const screenWidth = ref(window.innerWidth)
    const isConnected = ref(false)
    
    const responsiveColumns = computed(() => {
      if (screenWidth.value < 768) return 1
      if (screenWidth.value < 1024) return 2
      return 3
    })
    
    const connectionStatus = computed(() => {
      if (isConnected.value) {
        return {
          type: 'success',
          icon: 'SuccessFilled',
          text: t('home.connected')
        }
      } else {
        return {
          type: 'info',
          icon: 'CircleCloseFilled',
          text: t('home.notConnected')
        }
      }
    })
    
    const handleResize = () => {
      screenWidth.value = window.innerWidth
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
    })
    
    return {
      screenWidth,
      isConnected,
      responsiveColumns,
      connectionStatus,
      handleResize,
      t
    }
  },
  data() {
    return {
      backendUrl: import.meta.env.VITE_CHAINSTREAM_BACKEND_API,
      loading: false,
      runningAgentsCount: 0,
      activeStreamsCount: 0
    }
  },
  methods: {
    checkConn() {
      this.loading = true
      checkConnection()
        .then(res => {
          this.loading = false
          this.isConnected = true
          console.log(res)
          this.$message.success(this.t('home.connectionSuccess'))
        })
        .catch(err => {
          this.loading = false
          this.isConnected = false
          console.log(err)
          this.$message.error(this.t('home.connectionFailed'))
        })
    },
    
    copyUrl() {
      navigator.clipboard.writeText(this.backendUrl).then(() => {
        this.$message.success(this.t('home.urlCopied'))
      }).catch(() => {
        this.$message.error(this.t('home.urlCopyFailed'))
      })
    },
    
    refreshConfig() {
      this.checkConn()
    },
    
    async loadStatistics() {
      try {
        const response = await getStatistics()
        console.log('Statistics response:', response) // Debug log
        this.runningAgentsCount = response.running_agents_count
        this.activeStreamsCount = response.active_streams_count
      } catch (error) {
        console.error('Failed to load statistics:', error)
        this.runningAgentsCount = 0
        this.activeStreamsCount = 0
      }
    }
  },
  
  mounted() {
    this.loadStatistics()
    // Refresh statistics every 30 seconds
    this.statisticsInterval = setInterval(() => {
      this.loadStatistics()
    }, 30000)
  },
  
  beforeUnmount() {
    if (this.statisticsInterval) {
      clearInterval(this.statisticsInterval)
    }
  }
}

</script>


<style lang="scss" scoped>
.home-container {
  padding: 24px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 0;
}

.welcome-title {
  color: #2c3e50;
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 16px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-subtitle {
  color: #7f8c8d;
  font-size: 1.2rem;
  font-weight: 400;
  margin: 0;
}

.config-section {
  margin-bottom: 40px;
}

.config-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 1.2rem;
  color: #409EFF;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #303133;
}

.config-content {
  padding: 20px 0;
}

.connection-descriptions {
  :deep(.el-descriptions__title) {
    font-size: 1.1rem;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16px;
  }
  
  :deep(.desc-label) {
    font-weight: 600;
    color: #606266;
  }
}

.url-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.url-text {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.9rem;
  background: #f5f7fa;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
}

.copy-btn {
  background: #f0f9ff;
  border-color: #b3d8ff;
  color: #409EFF;
  
  &:hover {
    background: #e1f5fe;
    border-color: #81c784;
  }
}

.status-display {
  display: flex;
  align-items: center;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.stats-section {
  margin-bottom: 40px;
}

.stats-row {
  margin: 0;
}

.stat-col {
  margin-bottom: 16px;
}

.stat-card {
  border-radius: 12px;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  }
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #909399;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .home-container {
    padding: 20px;
  }
  
  .welcome-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .home-container {
    padding: 16px;
  }
  
  .welcome-section {
    margin-bottom: 30px;
    padding: 30px 0;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .config-section,
  .stats-section {
    margin-bottom: 30px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 8px;
  }
  
  .stat-content {
    gap: 12px;
  }
  
  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .home-container {
    padding: 12px;
  }
  
  .welcome-title {
    font-size: 1.8rem;
  }
  
  .welcome-subtitle {
    font-size: 0.9rem;
  }
  
  .card-title {
    font-size: 1rem;
  }
  
  .url-display {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .stat-content {
    flex-direction: column;
    text-align: center;
    gap: 8px;
  }
  
  .stat-icon {
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
  
  .stat-number {
    font-size: 1.3rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
}
</style>