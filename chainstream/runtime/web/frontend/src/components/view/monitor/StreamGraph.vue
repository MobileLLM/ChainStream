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
                <div class="stat-label">活跃流</div>
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
                <div class="stat-label">运行代理</div>
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
                <div class="stat-label">节点数</div>
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
                <div class="stat-label">连接数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-header>

    <!-- 主要内容区域 -->
    <el-container style="height: calc(100vh - 120px);">
      <!-- 左侧控制面板 -->
      <el-aside width="250px" style="padding: 0;">
        <el-card shadow="never" style="height: 100%; margin: 0;">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>控制面板</span>
              <el-switch
                v-model="autoRefresh"
                active-text="自动刷新"
                @change="toggleAutoRefresh"
                size="small"
              />
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 5px;">
              💡 边的宽度反映数据流量大小
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
              手动刷新
            </el-button>
            
            <el-divider />
            
            <div class="control-group">
              <label>刷新间隔</label>
              <el-select v-model="refreshInterval" @change="updateRefreshInterval" size="small" style="width: 100%;">
                <el-option label="5秒" :value="5000" />
                <el-option label="10秒" :value="10000" />
                <el-option label="30秒" :value="30000" />
                <el-option label="1分钟" :value="60000" />
              </el-select>
            </div>
            
            <el-divider />
            
            <div class="control-group">
              <label>布局算法</label>
              <el-select v-model="layoutType" @change="updateLayout" size="small" style="width: 100%;">
                <el-option label="垂直布局" value="vertical" />
                <el-option label="水平布局" value="horizontal" />
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
              <label>连接线曲率</label>
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
              <label>连接线透明度</label>
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
              <label>显示标签</label>
              <el-switch
                v-model="showLabels"
                @change="updateChartConfig"
                size="small"
              />
            </div>
            
            <el-divider />
            
<!--            <div class="control-group">-->
<!--              <label>标签字体大小</label>-->
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
<!--              <label>动画效果</label>-->
<!--              <el-switch-->
<!--                v-model="enableAnimation"-->
<!--                @change="updateChartConfig"-->
<!--                size="small"-->
<!--              />-->
<!--            </div>-->
<!--            -->
<!--            <el-divider />-->
            
            <div class="control-group">
              <label>固定颜色方案</label>
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
              <span>流图可视化</span>
              <div>
                <el-tag v-if="lastUpdateTime" type="info" size="small">
                  最后更新: {{ lastUpdateTime }}
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

export default {
  components: {
    Connection,
    User,
    CircleCheck,
    Link,
    Refresh
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
            formatter: function(params) {
              if (params.dataType === 'node') {
                const user = params.data.user || 'System';
                return `节点: ${params.name}<br/>用户: ${user}`;
              } else if (params.dataType === 'edge') {
                const value = params.data.value || 0;
                return `连接: ${params.data.source} → ${params.data.target}<br/>流量: ${value}/s`;
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
              formatter: function(params) {
                const user = params.data.user || 'System';
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
        this.$message.error('获取流图数据失败');
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

.chart-container {
  position: relative;
  height: calc(100vh - 220px);
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
@media (max-width: 768px) {
  .el-aside {
    width: 100% !important;
    height: auto !important;
  }
  
  .stat-value {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 12px;
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