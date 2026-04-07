<template>
  <el-container style="height: 100%; margin: 0; padding: 0;" direction="vertical">
    <!-- 顶部统计面板 -->
    <el-header height="120px" style="padding: 10px; background-color: #f5f5f5;">
      <el-row :gutter="20" style="height: 100%;">
        <el-col :span="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="24" color="#409EFF"><Connection /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.active_streams_count || 0 }}</div>
                <div class="stat-label">{{ $t('streamGraph.activeStreams') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="24" color="#67C23A"><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ statistics.running_agents_count || 0 }}</div>
                <div class="stat-label">{{ $t('streamGraph.runningAgents') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="24" color="#E6A23C"><CircleCheck /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ graphStats.nodeCount || 0 }}</div>
                <div class="stat-label">{{ $t('streamGraph.nodeCount') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon">
                <el-icon size="24" color="#F56C6C"><Link /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ graphStats.edgeCount || 0 }}</div>
                <div class="stat-label">{{ $t('streamGraph.edgeCount') }}</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-header>

    <!-- 主要内容区域 -->
    <el-container class="main-content-container">
      <!-- 左侧控制面板 -->
      <el-aside width="250px" style="padding: 0;" class="control-aside">
        <el-card shadow="never" style="height: 100%; margin: 0;">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>{{ $t('streamGraph.controlPanel') }}</span>
              <el-switch
                v-model="autoRefresh"
                :active-text="$t('streamGraph.autoRefresh')"
                @change="toggleAutoRefresh"
                size="small"
              />
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">
              {{ $t('streamGraph.edgeWidthHint') }}
            </div>
          </template>
          
          <div class="control-panel">
            <el-button 
              type="primary" 
              @click="getStreamGraphData" 
              :loading="loading"
              style="width: 100%; margin-bottom: 10px;"
            >
              <el-icon><Refresh /></el-icon>
              {{ $t('streamGraph.manualRefresh') }}
            </el-button>
            
            <el-divider />
            
            <div class="control-group">
              <label>{{ $t('streamGraph.refreshInterval') }}</label>
              <el-select v-model="refreshInterval" @change="updateRefreshInterval" size="small" style="width: 100%;">
                <el-option :label="`5${$t('streamGraph.seconds')}`" :value="5000" />
                <el-option :label="`10${$t('streamGraph.seconds')}`" :value="10000" />
                <el-option :label="`30${$t('streamGraph.seconds')}`" :value="30000" />
                <el-option :label="`1${$t('streamGraph.minute')}`" :value="60000" />
              </el-select>
            </div>
            
            <el-divider />
            
            <div class="control-group">
              <label>{{ $t('streamGraph.layoutAlgorithm') }}</label>
              <el-select v-model="layoutType" @change="updateLayout" size="small" style="width: 100%;">
                <el-option :label="$t('streamGraph.verticalLayout')" value="vertical" />
                <el-option :label="$t('streamGraph.horizontalLayout')" value="horizontal" />
              </el-select>
            </div>
            
            <el-divider />
            
<!--            <div class="control-group">-->
<!--              <label>节点间距</label>-->
<!--              <el-slider-->
<!--                v-model="nodeSpacing"-->
<!--                :min="10"-->
<!--                :max="100"-->
<!--                @change="updateNodeSpacing"-->
<!--                show-input-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
            
<!--            <el-divider />-->
            
<!--            <div class="control-group">-->
<!--              <label>节点宽度</label>-->
<!--              <el-slider-->
<!--                v-model="nodeWidth"-->
<!--                :min="10"-->
<!--                :max="50"-->
<!--                @change="updateChartConfig"-->
<!--                show-input-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
<!--            -->
<!--            <el-divider />-->
            
            <div class="control-group">
              <label>{{ $t('streamGraph.lineCurveness') }}</label>
              <el-slider
                v-model="lineCurveness"
                :min="0"
                :max="1"
                :step="0.1"
                @change="updateChartConfig"
                show-input
                size="small"
              />
            </div>
            
            <el-divider />
            
            <div class="control-group">
              <label>{{ $t('streamGraph.lineOpacity') }}</label>
              <el-slider
                v-model="lineOpacity"
                :min="0.1"
                :max="1"
                :step="0.1"
                @change="updateChartConfig"
                show-input
                size="small"
              />
            </div>
            
<!--            <div class="control-group">-->
<!--              <label>边最小宽度</label>-->
<!--              <el-slider-->
<!--                v-model="minEdgeWidth"-->
<!--                :min="1"-->
<!--                :max="10"-->
<!--                :step="1"-->
<!--                @change="updateChartConfig"-->
<!--                show-input-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
            
<!--            <div class="control-group">-->
<!--              <label>边最大宽度</label>-->
<!--              <el-slider-->
<!--                v-model="maxEdgeWidth"-->
<!--                :min="10"-->
<!--                :max="50"-->
<!--                :step="2"-->
<!--                @change="updateChartConfig"-->
<!--                show-input-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
            
<!--            <el-divider />-->
            
            <div class="control-group">
              <label>{{ $t('streamGraph.showLabels') }}</label>
              <el-switch
                v-model="showLabels"
                @change="updateChartConfig"
                size="small"
              />
            </div>
            
            <el-divider />
            
<!--            <div class="control-group">-->
<!--              <label>{{ $t('streamGraph.labelFontSize') }}</label>-->
<!--              <el-slider-->
<!--                v-model="labelFontSize"-->
<!--                :min="8"-->
<!--                :max="16"-->
<!--                @change="updateChartConfig"-->
<!--                show-input-->
<!--                size="small"-->
<!--                :disabled="!showLabels"-->
<!--              />-->
<!--            </div>-->
            
<!--            <el-divider />-->
            
<!--            <div class="control-group">-->
<!--              <label>{{ $t('streamGraph.animation') }}</label>-->
<!--              <el-switch-->
<!--                v-model="enableAnimation"-->
<!--                @change="updateChartConfig"-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
<!--            -->
<!--            <el-divider />-->
            
            <div class="control-group">
              <label>{{ $t('streamGraph.fixedColors') }}</label>
              <el-switch
                v-model="fixedColors"
                @change="updateChartConfig"
                size="small"
              />
            </div>
            
            <el-divider />
            
<!--            <div class="control-group">-->
<!--              <label>拖拽功能</label>-->
<!--              <el-switch-->
<!--                v-model="enableDrag"-->
<!--                @change="updateChartConfig"-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
          </div>
        </el-card>
      </el-aside>

      <!-- 图表区域 -->
      <el-main style="padding: 0;">
        <el-card shadow="never" style="height: 100%; margin: 0;">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>{{ $t('streamGraph.visualization') }}</span>
              <div>
                <el-tag v-if="lastUpdateTime" type="info" size="small">
                  {{ $t('streamGraph.lastUpdate') }}: {{ lastUpdateTime }}
                </el-tag>
              </div>
            </div>
          </template>
          
          <div class="chart-container">
            <div class="chart-content" ref="chartContent"></div>
        </div>
        </el-card>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import * as echarts from 'echarts';
import { getStreamGraphData } from '@/api/monitor/streamGraph.js';
import { getStatistics } from '@/api/monitor/statistics.js';
import { Connection, User, CircleCheck, Link, Refresh } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';

export default {
  components: {
    Connection,
    User,
    CircleCheck,
    Link,
    Refresh
  },
  setup() {
    const { t } = useI18n()
    return { t }
  },
  data() {
    return {
      chartNode: [],
      chartEdge: [],
      loading: false,
      autoRefresh: false,
      refreshTimer: null,
      refreshInterval: 10000, // 默认10秒
      layoutType: 'vertical',
      nodeSpacing: 50,
      nodeWidth: 20,
      lineCurveness: 0.5,
      lineOpacity: 0.6,
      minEdgeWidth: 2,
      maxEdgeWidth: 20,
      showLabels: true,
      labelFontSize: 11,
      enableAnimation: true,
      fixedColors: true,
      enableDrag: true,
      lastUpdateTime: null,
      statistics: {
        active_streams_count: 0,
        running_agents_count: 0
      },
      graphStats: {
        nodeCount: 0,
        edgeCount: 0
      },
      // 固定的颜色方案
      fixedColorPalette: [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
        '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc', '#ff9f7f'
      ]
    }
  },
  mounted() {
    this.drawChart();
    this.getStatistics();
    this.getStreamGraphData();
  },
  beforeUnmount() {
    this.clearRefreshTimer();
  },
  methods: {
    drawChart() {
      if (!this.$refs.chartContent) {
        console.warn('Chart content element not found');
        return;
      }
      
      var myChart = echarts.init(this.$refs.chartContent);

      // 为节点分配固定颜色
      const nodesWithColors = this.chartNode.map((node, index) => {
        if (this.fixedColors) {
          return {
            ...node,
            itemStyle: {
              color: this.fixedColorPalette[index % this.fixedColorPalette.length],
              borderWidth: 1,
              borderColor: '#aaa'
            }
          };
        }
        return {
          ...node,
          itemStyle: {
            borderWidth: 1,
            borderColor: '#aaa'
          }
        };
      });

      var option = {
          tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove',
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            borderColor: '#333',
            borderWidth: 1,
            textStyle: {
              color: '#fff',
              fontSize: 12
            },
            formatter: (params) => {
              if (params.dataType === 'node') {
                const user = params.data.user || this.t('common.system');
                return `${this.t('streamGraph.node')}: ${params.name}<br/>${this.t('streamGraph.user')}: ${user}`;
              } else if (params.dataType === 'edge') {
                const value = params.data.value || 0;
                return `${this.t('streamGraph.connection')}: ${params.data.source} → ${params.data.target}<br/>${this.t('streamGraph.traffic')}: ${value}/s`;
              }
              return params.name;
            }
          },
        animation: this.enableAnimation,
        animationDuration: this.enableAnimation ? 1000 : 0,
          series: [
            {
              type: 'sankey',
            layout: 'none',
            data: nodesWithColors,
            links: this.chartEdge,
            orient: this.layoutType,
              emphasis: {
                focus: 'adjacency'
              },
              label: {
              position: 'top',
              show: this.showLabels,
              fontSize: this.labelFontSize,
              formatter: (params) => {
                const user = params.data.user || this.t('common.system');
                const name = params.name.length > 15 ? params.name.substring(0, 15) + '...' : params.name;
                return `${name}\n(${user})`;
              }
            },
            lineStyle: {
              color: this.fixedColors ? 'source' : 'gradient',
              curveness: this.lineCurveness,
              opacity: this.lineOpacity,
              width: function(params) {
                // 根据流量大小设置边的宽度
                const value = params.data.value || 1;
                const minValue = 1;
                const maxValue = Math.max(...this.chartEdge.map(edge => edge.value || 1));
                
                if (maxValue === minValue) return this.minEdgeWidth;
                
                const ratio = (value - minValue) / (maxValue - minValue);
                return this.minEdgeWidth + (this.maxEdgeWidth - this.minEdgeWidth) * ratio;
              }.bind(this)
            },
            itemStyle: {
              borderWidth: 1,
              borderColor: '#aaa'
            },
            nodeGap: this.nodeSpacing,
            nodeWidth: this.nodeWidth,
            nodeAlign: 'left',  // 改为left对齐，可以减少重叠
            // 拖拽功能控制
            draggable: this.enableDrag,
            focusNodeAdjacency: true,
            // 增加节点间距防止重叠
            layoutIterations: 32,  // 增加布局迭代次数，改善布局质量
            left: '5%',
            right: '5%',
            top: '5%',
            bottom: '5%'
          }
        ]
      };
      
    myChart.setOption(option);
      
      // 监听窗口大小变化
      window.addEventListener('resize', () => {
        myChart.resize();
      });
    },
    
    getStreamGraphData() {
      this.loading = true;
      getStreamGraphData().then(res => {
        console.log('StreamGraph API Response:', res);
        
        // 转换数据格式为Sankey图需要的格式
        this.chartNode = res.node || [];
        this.chartEdge = (res.edge || []).map(edge => ({
          source: edge.source || edge.from,
          target: edge.target || edge.to,
          value: edge.value || 1
        }));
        
        // 更新统计信息
        this.graphStats.nodeCount = this.chartNode.length;
        this.graphStats.edgeCount = this.chartEdge.length;
        
        // 更新最后更新时间
        this.lastUpdateTime = new Date().toLocaleTimeString();
        
        this.drawChart(); // 在数据更新后重新绘制图表
        this.loading = false;
      }).catch(error => {
        console.error('StreamGraph API Error:', error);
        this.loading = false;
        this.$message.error(this.t('streamGraph.getDataFailed'));
      });
    },
    
    getStatistics() {
      getStatistics().then(res => {
        this.statistics = res;
      }).catch(error => {
        console.error('Statistics API Error:', error);
      });
    },
    
    toggleAutoRefresh() {
      if (this.autoRefresh) {
        this.startAutoRefresh();
      } else {
        this.clearRefreshTimer();
      }
    },
    
    startAutoRefresh() {
      this.clearRefreshTimer();
      this.refreshTimer = setInterval(() => {
        this.getStreamGraphData();
        this.getStatistics();
      }, this.refreshInterval);
    },
    
    clearRefreshTimer() {
      if (this.refreshTimer) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = null;
      }
    },
    
    updateRefreshInterval() {
      if (this.autoRefresh) {
        this.startAutoRefresh();
      }
    },
    
    updateLayout() {
      this.drawChart();
    },
    
    updateNodeSpacing() {
      this.drawChart();
    },
    
    updateChartConfig() {
      this.drawChart();
    }
  }
}

</script>

<style scoped>
.stat-card {
  height: 100%;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-card:hover {
  transform: translateY(-2px);
  transition: transform 0.3s ease;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
}

.stat-icon {
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f9ff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  line-height: 1;
}

.control-panel {
  height: calc(100% - 80px);
  overflow-y: auto;
  padding: 0 10px;
}

.control-group {
  margin-bottom: 20px;
}

.control-group:last-child {
  margin-bottom: 0;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.el-header {
  border-bottom: 1px solid #e4e7ed;
}

.main-content-container {
  height: calc(100vh - 180px);
  min-height: 500px;
}

.control-aside {
  border-right: 1px solid #e4e7ed;
}

.chart-container {
  position: relative;
  height: calc(100vh - 280px);
  min-height: 400px;
  overflow: hidden;
  background-color: #fff;
  border-radius: 4px;
  margin-bottom: 15px;
}

.chart-content {
  width: 100%;
  height: 100%;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .el-header {
    height: auto !important;
    padding: 8px !important;
  }
  
  .el-row {
    flex-wrap: wrap;
  }
  
  .stat-card .stat-content {
    padding: 8px;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 12px;
  }
}

@media (max-width: 768px) {
  .el-header {
    height: auto !important;
    padding: 10px 5px !important;
  }
  
  .el-row {
    display: grid !important;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .el-col {
    width: 100% !important;
  }
  
  .main-content-container {
    height: auto !important;
    min-height: 600px;
    flex-direction: column;
  }
  
  .el-aside {
    width: 100% !important;
    max-height: 300px;
    overflow-y: auto;
  }
  
  .el-main {
    padding: 10px !important;
  }
  
  .chart-container {
    height: calc(100vh - 520px) !important;
    min-height: 400px;
  }
  
  .control-panel {
    max-height: 200px;
  }
  
  .stat-value {
    font-size: 18px;
  }
  
  .stat-label {
    font-size: 11px;
  }
  
  .stat-icon {
    width: 32px;
    height: 32px;
  }
}

@media (max-width: 480px) {
  .el-row {
    grid-template-columns: 1fr !important;
  }
  
  .stat-value {
    font-size: 16px;
  }
  
  .stat-label {
    font-size: 10px;
  }
  
  .control-group label {
    font-size: 12px;
  }
  
  .chart-container {
    height: calc(100vh - 600px) !important;
    min-height: 300px;
  }
}

/* 滚动条样式 */
.control-panel::-webkit-scrollbar {
  width: 4px;
}

.control-panel::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.control-panel::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.control-panel::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>