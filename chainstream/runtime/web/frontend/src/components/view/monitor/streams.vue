<script setup>
import $ from 'jquery';
</script>

<template>
<el-container style="height: 100%; margin: 0; padding: 0;" direction="vertical">
  <div class="filter-container" style="margin-bottom: 10px; height: 40px;">
    <el-button type="primary" @click="fetchStreams">刷新</el-button>
  </div>
  <el-scrollbar style="height: calc(100% - 80px); width: 100%;">
    <el-table :height="elTableHeight" v-loading="loading" :data="streams" style="width: 100%;" table-layout="auto">
      <el-table-column type="index" label="#" width="60"></el-table-column>
      <el-table-column prop="stream_id" label="流ID" min-width="150" show-overflow-tooltip></el-table-column>
      <el-table-column prop="user" label="用户" width="120">
        <template #default="scope">
          <el-tag v-if="scope.row.user" type="primary" size="small">{{ scope.row.user }}</el-tag>
          <el-tag v-else type="info" size="small">系统</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="创建时间" width="160"></el-table-column>
      <el-table-column prop="create_by" label="创建者" width="150" show-overflow-tooltip></el-table-column>
      <el-table-column prop="encryption_enabled" label="加密" width="80">
        <template #default="scope">
          <el-tag v-if="scope.row.encryption_enabled" type="success" size="small">是</el-tag>
          <el-tag v-else type="info" size="small">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="listeners" label="监听者" min-width="200" show-overflow-tooltip>
        <template #default="scope">
          <el-tag v-if="scope.row.listeners && scope.row.listeners.length > 0" 
                  v-for="(listener, index) in scope.row.listeners" 
                  :key="index" 
                  type="warning" 
                  size="small" 
                  style="margin-right: 5px; margin-bottom: 2px;">
            {{ listener }}
          </el-tag>
          <span v-else style="color: #999;">无</span>
        </template>
      </el-table-column>
    </el-table>
  </el-scrollbar>
</el-container>
</template>

<script>
import { getStreams } from "@/api/monitor/streams.js";

export default {
  data() {
    return {
      loading: false,
      streams: [],
      elTableHeight: $('.el-scrollbar').height(),
    }
  },
  created() {
    this.loading = true;
    this.fetchStreams();
    window.addEventListener('resize', this.handleHightChange);
  },
  destroyed() {
    window.removeEventListener('resize', this.handleHightChange);
  },
  methods: {
    fetchStreams() {
      this.loading = true;
      getStreams().then(res => {
        this.streams = this.processStreamData(res);
        this.$message.success("获取流信息成功");
        this.loading = false;
      }).catch(err => {
        console.log(err);
        this.$message.error("获取流信息失败");
        this.loading = false;
      });
    },
    processStreamData(streams) {
      // 处理流数据，确保所有字段都有合适的默认值
      return streams.map(stream => ({
        ...stream,
        user: stream.user || null,
        create_by: stream.create_by || '未知',
        encryption_enabled: stream.encryption_enabled || false,
        listeners: stream.listeners || []
      }));
    },
    handleHightChange() {
      this.elTableHeight = $('.el-scrollbar').height();
    }
  }
}
</script>

<style scoped>
.filter-container {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-table .el-table__header {
  background-color: #f5f7fa;
}

.el-table .el-table__row:hover {
  background-color: #f0f9ff;
}

.el-tag {
  margin: 1px;
}

.el-scrollbar {
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}
</style>