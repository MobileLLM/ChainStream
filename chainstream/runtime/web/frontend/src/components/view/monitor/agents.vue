<script setup>
import $ from 'jquery'
</script>


<template>
  <el-container style="height: 100%; margin: 0; padding: 0">
    <el-aside :height="elTableHeight" width="30%" style="margin: 0 1% 0 0; padding: 0">
      <el-scrollbar style="height: 100%; width: 100%; margin: 0; padding: 0">
<!--        <el-table v-loading="path_loading" :data="agents_path" :height="elTableHeight" style="width: 100%; margin: 0; padding: 0" table-layout="auto" >-->
<!--          <el-table-column prop="agent_path" label="Path" width="180"></el-table-column>-->
<!--          <el-table-column align="right">-->
<!--            <template #default="scope">-->
<!--              <el-button size="small" type="success" @click="handleStart(scope.$index, scope.row)">Start</el-button>-->
<!--            </template>-->
<!--          </el-table-column>-->
<!--        </el-table>-->
        <el-tree :data="agents_path" :props="defaultProps" show-checkbox @check-change="handleCheckChange">
<!--          <template #default="{ node, data }">-->
<!--            <span class="custom-tree-node" style="flex: 1; display: flex; align-items: center; justify-content: space-between; font-size: 14px; padding-right: 8px;">-->
<!--              <span>{{ node.label }}</span>-->
<!--              <el-button size="small" type="success" @click="handleStart(data)">Start</el-button>-->
<!--            </span>-->
<!--          </template>-->
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
import {startAgent, stopAgent, getAgentsPath} from '@/api/monitor/agents.js'
import {formToJSON} from "axios";

export  default {
  data() {
    return {
      path_loading: true,
      running_loading: true,
      agents_path: [],
      defaultProps: {
        children: "children",
        label: "label",
        disabled: "disabled"
      },
      agents_running: [],
      elTableHeight: $('.el-scrollbar').height(),
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
    handleCheckChange(data, checked, indeterminate) {

    },
    getAgentsList() {
      this.path_loading = true
      getAgentsPath().then(res => {
        // this.agents_path = this.convertProxyToPlainObject(res.data)
        this.agents_path = res.data
        console.log(this.agents_path)
        this.path_loading = false
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