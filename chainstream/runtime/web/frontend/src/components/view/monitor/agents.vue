<script setup>
import $ from 'jquery'
</script>


<template>
  <el-container style="height: 100%; margin: 0; padding: 0">
    <el-aside :height="elTableHeight" width="20%" style="margin: 0 1% 0 0; padding: 0">
      <el-scrollbar style="height: 100%; width: 100%; margin: 0; padding: 0">
<!--        <el-table v-loading="path_loading" :data="agents_path" :height="elTableHeight" style="width: 100%; margin: 0; padding: 0" table-layout="auto" >-->
<!--          <el-table-column prop="agent_path" label="Path" width="180"></el-table-column>-->
<!--          <el-table-column align="right">-->
<!--            <template #default="scope">-->
<!--              <el-button size="small" type="success" @click="handleStart(scope.$index, scope.row)">Start</el-button>-->
<!--            </template>-->
<!--          </el-table-column>-->
<!--        </el-table>-->
<!--        <el-button type="primary" @click="handleStart">开始</el-button>-->
        <el-tree :data="agents_path" :props="defaultProps" default-expand-all>
          <template #default="{ node, data }">
            <span class="custom-tree-node" style="flex: 1; display: flex; align-items: center; justify-content: space-between; font-size: 14px; padding-right: 8px;">
              <span>{{ node.label }}</span>
              <el-button v-if="!data.disabled && !data.is_running" size="small" type="success" @click="handleTreeStart(data)">Start</el-button>
<!--              <el-button v-if="data.is_running" size="small" type="warning">Running</el-button>-->
              <el-button v-if="data.is_running" size="small" type="warning" @click="handleTreeStop(data)">Stop</el-button>
            </span>
          </template>
        </el-tree>

      </el-scrollbar>
    </el-aside>
    <el-scrollbar style="height: 100%; width: 100%; margin: 0; padding: 0">
      <el-table v-loading="running_loading" :data="agents_running" :height="elTableHeight" style="width: 100%; margin: 0; padding: 0" table-layout="auto" >
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
          <el-table-column prop="running_time" label="Running Time"></el-table-column>
        </el-table-column>
<!--        <el-table-column align="right">-->
<!--          <template #default="scope">-->
<!--            <el-button size="small" type="success" @click="handleStart(scope.$index, scope.row)">Start</el-button>-->
<!--            <el-button size="small" type="danger" @click="handleStop(scope.$index, scope.row)">Stop</el-button>-->
<!--          </template>-->
<!--        </el-table-column>-->
      </el-table>
    </el-scrollbar>
  </el-container>
</template>


<script>
import {startAgent, stopAgent, getAgentsPath, getRunningAgents} from '@/api/monitor/agents.js'
import {formToJSON} from "axios";

export  default {
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
            agent_path: 'C:\\Program Files\\Agent\\agent.exe',
            description: 'This is a moke agent',
            version: '1.0.0',
            type: 'user',
            status: 'running',
            running_time: '2021-11-11 11:11:11',
            is_running: true,
          },
      ],
      elTableHeight: $('.el-scrollbar').height(),
    }
  },
  created() {
    this.getAgentsList()
    window.addEventListener('resize', this.handleHightChange);
    // this.getRunningAgentsList()
  },
  destroyed() {
    window.removeEventListener('resize', this.handleHightChange);
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
        // this.agents_running = this.convertProxyToPlainObject(res.data)
        this.agents_running = res.data
        this.running_loading = false
      })
    },
    getAgentsList() {
      this.path_loading = true
      getAgentsPath().then(res => {
        // this.agents_path = this.convertProxyToPlainObject(res.data)
        this.agents_path = res.data
        this.path_loading = false
      })
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
        if (res.data['res'] === 'ok') {
          this.$message.success('Agent started successfully')
          this.getAgentsList()
        } else {
          this.$message.error('Agent start failed')
          this.getAgentsList()
        }
      })
    },
    handleTreeStop(data) {
      stopAgent(data.label).then(res => {
        if (res.data['res'] === 'ok') {
          this.$message.success('Agent stopped successfully')
          this.getAgentsList()
        } else {
          this.$message.error('Agent stop failed')
          this.getAgentsList()
        }
      })
    },
    handleStart(index, row) {

    },
    handleStop(index, row) {

    },
    filterType(value, row) {
      return row.type === value
    },
    filterStatus(value, row) {
      return row.status === value
    },
    handleHightChange() {
      this.elTableHeight = $('.el-scrollbar').height();
    },
  },

  // mounted() {
  //   this.elTableHeight = $('.el-scrollbar').height();
  // }
}
</script>

<style scoped>




</style>