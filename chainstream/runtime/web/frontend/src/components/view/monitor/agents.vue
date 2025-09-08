<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Refresh, VideoPlay, VideoPause } from '@element-plus/icons-vue'
import $ from 'jquery'
</script>


<template>
  <div class="agents-container">
    <el-row :gutter="16" class="agents-row">
      <!-- Agent Tree Panel: Static code view for starting agents -->
      <el-col :span="8" class="tree-panel">
        <el-card class="tree-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">Agent Tree</span>
              <el-button 
                type="primary" 
                size="small" 
                :icon="Refresh"
                @click="getAgentsList"
                :loading="path_loading"
              >
                Refresh
              </el-button>
            </div>
          </template>
          
          <div class="tree-content">
            <div v-if="!agents_path || agents_path.length === 0" class="empty-state">
              <el-empty description="No agents found" :image-size="80" />
            </div>
            <div v-else class="tree-wrapper">
              <!-- Debug info -->
              <!-- <div style="font-size: 12px; color: #999; padding: 4px; background: #f5f5f5;">
                Tree Height: {{ treeHeight }}px, Screen Width: {{ screenWidth }}px, Data Count: {{ agents_path.length }}
              </div> -->
              <el-tree 
                :data="agents_path" 
                :props="defaultProps" 
                default-expand-all
                class="agent-tree"
                node-key="label"
                :expand-on-click-node="false"
              >
                <template #default="{ node, data }">
                  <div class="tree-node">
                    <el-tooltip 
                      :content="node.label" 
                      placement="top" 
                      :disabled="node.label.length <= 20"
                      effect="dark"
                    >
                      <span class="node-label">{{ node.label }}</span>
                    </el-tooltip>
                    <div class="node-actions">
                      <el-button 
                        v-if="!data.disabled" 
                        size="small" 
                        type="success" 
                        @click="handleTreeStart(data)"
                        :icon="VideoPlay"
                        class="action-btn"
                      >
                        Start
                      </el-button>
                    </div>
                  </div>
                </template>
              </el-tree>
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- Running Agents Table: Dynamic management of running agents -->
      <el-col :span="16" class="table-panel">
        <el-card class="table-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">Running Agents</span>
              <div class="header-actions">
                <el-button 
                  type="primary" 
                  size="small" 
                  :icon="Refresh"
                  @click="getRunningAgentsList"
                  :loading="running_loading"
                >
                  Refresh
                </el-button>
              </div>
            </div>
          </template>
          
          <div class="table-content">
            <el-table 
              v-loading="running_loading" 
              :data="agents_running" 
              class="agents-table"
              stripe
              border
              :height="tableHeight"
              style="width: 100%"
            >
              <el-table-column type="index" label="#" width="60" fixed="left" />
              
              <el-table-column prop="agent_id" label="Agent ID" width="180" fixed="left">
                <template #default="scope">
                  <el-text class="agent-id" type="primary">{{ scope.row.agent_id }}</el-text>
                </template>
              </el-table-column>
              
              <el-table-column prop="agent_file_path" label="Path" min-width="200" show-overflow-tooltip>
                <template #default="scope">
                  <el-text class="file-path">{{ scope.row.agent_file_path }}</el-text>
                </template>
              </el-table-column>
              
              <el-table-column prop="description" label="Description" min-width="150" show-overflow-tooltip>
                <template #default="scope">
                  <el-text>{{ scope.row.description }}</el-text>
                </template>
              </el-table-column>
              
              <el-table-column prop="version" label="Version" width="100" align="center">
                <template #default="scope">
                  <el-tag size="small" type="info">{{ scope.row.version }}</el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="user" label="User" width="120" align="center">
                <template #default="scope">
                  <el-tag 
                    v-if="scope.row.user"
                    size="small" 
                    type="warning"
                  >
                    {{ scope.row.user }}
                  </el-tag>
                  <el-tag 
                    v-else
                    size="small" 
                    type="info"
                  >
                    System
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column 
                prop="type"
                label="Type"
                width="100"
                align="center"
                :filters="[
                  { text: 'System', value: 'system' },
                  { text: 'User', value: 'user' },
                ]"
                :filter-method="filterType"
              >
                <template #default="scope">
                  <el-tag 
                    :type="scope.row.type === 'system' ? 'success' : 'primary'"
                    size="small"
                  >
                    {{ scope.row.type }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column 
                prop="status"
                label="Status"
                width="120"
                align="center"
                :filters="[
                  { text: 'Running', value: 'running' },
                  { text: 'Stopped', value: 'stopped' },
                  { text: 'Error', value: 'error' }
                ]"
                :filter-method="filterStatus"
              >
                <template #default="scope">
                  <el-tag 
                    :type="getStatusType(scope.row.status)"
                    size="small"
                  >
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              
              <el-table-column prop="created_at" label="Created Time" width="180" align="center">
                <template #default="scope">
                  <el-text class="created-time">{{ formatTime(scope.row.created_at) }}</el-text>
                </template>
              </el-table-column>
              
              <el-table-column label="Actions" width="120" align="center" fixed="right">
                <template #default="scope">
                  <el-button 
                    v-if="scope.row.status === 'running'"
                    size="small" 
                    type="danger" 
                    @click="handleStop(scope.$index, scope.row)"
                    :icon="VideoPause"
                  >
                    Stop
                  </el-button>
                  <el-button 
                    v-else-if="scope.row.status === 'stopped'"
                    size="small" 
                    type="success" 
                    @click="handleStart(scope.$index, scope.row)"
                    :icon="VideoPlay"
                  >
                    Start
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import {startAgent, stopAgent, getAgentsPath, getRunningAgents} from '@/api/monitor/agents.js'
import {formToJSON} from "axios";

export default {
  data() {
    return {
      path_loading: true,
      running_loading: false,
      agents_path: [],
      checkedNodes: [],
      defaultProps: {
        children: "children",
        label: "label",
        disabled: "disabled",
        is_running: "is_running",
      },
      agents_running: [
          {
            agent_id: '123456',
            agent_file_path: 'C:\\Program Files\\Agent\\agent.exe',
            description: 'This is a mock agent',
            version: '1.0.0',
            type: 'user',
            user: 'admin',
            status: 'running',
            created_at: '2021-11-11 11:11:11',
            is_running: true,
          },
      ],
    }
  },
  computed: {
    // 计算表格高度，让表格自适应容器高度
    tableHeight() {
      // 计算可用高度：视口高度 - 容器padding - 卡片header - 卡片padding
      return window.innerHeight - 32 - 60 - 32; // 大约减去124px的固定高度
    }
  },
  created() {
    this.getAgentsList()
  },
  methods: {
    // convertProxyToPlainObject(proxy) {
    //   if (typeof proxy !== 'object' || proxy === null) {
    //     return proxy;
    //   }
    //   const plainObject = Array.isArray(proxy) ? [] : {};
    //   for (const key in proxy) {
    //     if (proxy.hasOwnProperty(key)) {
    //       plainObject[key] = this.convertProxyToPlainObject(proxy[key]);
    //     }
    //   }
    //   return plainObject;
    // },
    handleCheck(data) {
      this.checkedNodes = checkedNodes;
    },

    getRunningAgentsList() {
      this.running_loading = true
      getRunningAgents().then(res => {
        // this.agents_running = this.convertProxyToPlainObject(res)
        this.agents_running = res
        this.running_loading = false
      })
    },
    getAgentsList() {
      this.path_loading = true
      getAgentsPath().then(res => {
        console.log('API Response:', res)
        // this.agents_path = this.convertProxyToPlainObject(res)
        this.agents_path = res
        console.log('agents_path after assignment:', this.agents_path)
        this.path_loading = false
      }).catch(error => {
        console.error('Error fetching agents:', error)
        this.path_loading = false
      })
      this.getRunningAgentsList()
    },
    // handleTreeStart() {
    //   // const selectedNodes = this.checkedNodes.map(node => ({
    //   //   label: node.label // 假设节点有一个label属性
    //   //   // 可以根据实际情况添加更多需要发送给后端的数据
    //   // }));
    //   this.checkedNodes.forEach(node => {
    //     const data = {
    //       agent_id: node.data.agent_id,
    //       agent_path: node.data.agent_path,
    //       description: node.data.description,
    //
    //
    //     }
    //   }
    // },
    handleTreeStart(data) {
      startAgent(data.label).then(res => {
        if (res['res'] === 'ok') {
          this.$message.success('Agent started successfully')
          // 同时刷新agent tree和running agents表格
          this.getAgentsList()
          this.getRunningAgentsList()
        } else {
          this.$message.error('Agent start failed')
          this.getAgentsList()
        }
      }).catch(error => {
        this.$message.error('Agent start failed: ' + error.message)
        this.getAgentsList()
      })
    },
    handleStart(index, row) {
      startAgent(row.agent_id).then(res => {
        if (res['res'] === 'ok') {
          this.$message.success('Agent started successfully')
          // 刷新running agents表格
          this.getRunningAgentsList()
        } else {
          this.$message.error('Agent start failed')
        }
      }).catch(error => {
        this.$message.error('Agent start failed: ' + error.message)
      })
    },
    handleStop(index, row) {
      stopAgent(row.agent_id).then(res => {
        if (res['res'] === 'ok') {
          this.$message.success('Agent stopped successfully')
          // 刷新running agents表格
          this.getRunningAgentsList()
        } else {
          this.$message.error('Agent stop failed')
        }
      }).catch(error => {
        this.$message.error('Agent stop failed: ' + error.message)
      })
    },
    filterType(value, row) {
      return row.type === value
    },
    filterStatus(value, row) {
      return row.status === value
    },
    getStatusType(status) {
      const statusMap = {
        'running': 'success',
        'stopped': 'info',
        'error': 'danger'
      };
      return statusMap[status] || 'info';
    },
    formatTime(timeString) {
      if (!timeString) return '-';
      try {
        const date = new Date(timeString);
        return date.toLocaleString();
      } catch (error) {
        return timeString;
      }
    },
  },

  // mounted() {
  //   this.elTableHeight = $('.el-scrollbar').height();
  // }
}
</script>

<style lang="scss" scoped>
.agents-container {
  padding: 16px;
  background-color: #f5f7fa;
  height: 100vh;
  box-sizing: border-box;
}

.agents-row {
  height: 100%;
}

.tree-panel,
.table-panel {
  height: 100%;
}

.tree-card,
.table-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.tree-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* 允许flex子元素收缩 */
  height: 100%; /* 确保占满父容器高度 */
}

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.tree-wrapper {
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background: #fff;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
  height: 100%; /* 占满父容器高度 */
}

.agent-tree {
  padding: 8px;
  
  :deep(.el-tree-node__content) {
    height: 48px;
    border-radius: 4px;
    margin: 2px 4px;
    padding: 0 8px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    
    &:hover {
      background-color: #f0f9ff;
      border-color: #b3d8ff;
    }
  }
  
  :deep(.el-tree-node__expand-icon) {
    color: #606266;
    font-size: 14px;
  }
  
  :deep(.el-tree-node__label) {
    font-size: 0.9rem;
    color: #303133;
  }
}

.tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 32px;
  gap: 8px;
}

.node-label {
  flex: 1;
  font-size: 0.9rem;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
  line-height: 1.4;
  padding: 2px 0;
}

.node-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  align-items: center;
}

.action-btn {
  min-width: 60px;
  height: 28px;
  font-size: 0.8rem;
  padding: 4px 8px;
  
  .el-icon {
    font-size: 12px;
  }
}

.table-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.agents-table {
  :deep(.el-table__header) {
    background-color: #fafafa;
  }
  
  :deep(.el-table__row) {
    &:hover {
      background-color: #f0f9ff;
    }
  }
}

.agent-id {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.85rem;
}

.file-path {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.8rem;
  color: #606266;
}

.created-time {
  font-size: 0.85rem;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .agents-container {
    padding: 8px;
    height: 100vh;
  }
  
  .agents-row {
    height: 100%;
  }
  
  .tree-panel,
  .table-panel {
    height: 50%;
  }
  
  .tree-card,
  .table-card {
    height: 100%;
  }
}
</style>