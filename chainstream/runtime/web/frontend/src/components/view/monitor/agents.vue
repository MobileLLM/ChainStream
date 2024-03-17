<script setup>
import $ from 'jquery'
</script>


<template>
  <el-container style="height: 100%; margin: 0; padding: 0">
    <el-scrollbar style="height: 100%; width: 100%">
      <el-table v-loading="loading" :data="agents" :height="elTableHeight" style="width: 100%;" table-layout="auto">
        <el-table-column type="index" label="#" width="50" />
        <el-table-column prop="agent_id" label="Agent ID" width="180">
        </el-table-column>
        <el-table-column label="Info">
          <el-table-column prop="agent_path" label="Path" width="180"></el-table-column>
          <el-table-column prop="description" label="Description" width="180"></el-table-column>
          <el-table-column prop="version" label="Version" width="120"></el-table-column>
          <el-table-column prop="type"
                           label="Type"
                           width="120"
                           :filters="[
                            { text: 'system', value: 'system' },
                            { text: 'user', value: 'user' },
                          ]"
                           :filter-method="filterType"
          >
            <template #default="scope">
                  <el-tag>{{ scope.row.type }}</el-tag>
            </template>
          </el-table-column>
        </el-table-column>
        <el-table-column label="Status">
          <el-table-column prop="status"
                           label="Status"
                           width="120"
                           :filters="[
                            { text: 'Running', value: 'running' },
                            { text: 'Stopped', value: 'stopped' },
                            { text: 'Error', value: 'error' }
                          ]"
                           :filter-method="filterStatus"
          >
            <template #default="scope">
              <el-tag type="warning">{{ scope.row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="running_time" label="Running Time" width="180"></el-table-column>
        </el-table-column>
        <el-table-column align="right">
          <template #default="scope">
            <el-button size="small" type="success" @click="handleStart(scope.$index, scope.row)">Start</el-button>
            <el-button size="small" type="danger" @click="handleStop(scope.$index, scope.row)">Stop</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-scrollbar>
  </el-container>
</template>


<script>
import { getAgents } from '@/api/monitor/agents.js'

export  default {
  data() {
    return {
      loading: true,
      agents: [],
      elTableHeight: $('.el-scrollbar').height(),
    }
  },
  created() {
    this.getAgentsList()
  },
  methods: {
    getAgentsList() {
      this.loading = true
      getAgents().then(res => {
        this.agents = res.data
        this.loading = false
      })
    },
    handleStart(index, row) {
      console.log(index, row)
    },
    handleStop(index, row) {
      console.log(index, row)
    },
    filterType(value, row) {
      return row.type === value
    },
    filterStatus(value, row) {
      return row.status === value
    },

  },
  mounted() {
    this.elTableHeight = $('.el-scrollbar').height();
  }
}
</script>

<style scoped>




</style>