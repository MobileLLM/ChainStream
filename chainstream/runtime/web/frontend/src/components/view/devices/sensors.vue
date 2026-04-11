<script setup>
import $ from 'jquery'
</script>

<template>
<el-container style="height: 100%; margin: 0; padding: 0;">
  <el-scrollbar>
    <el-table :height="elTableHeight" v-loading="loading" :data="sensors" style="width: 100%;" table-layout="auto">
      <el-table-column type="index" label="#" width="100"></el-table-column>
      <el-table-column prop="sensor_id" label="Sensor ID" width="150"></el-table-column>
      <el-table-column prop="sensor_name" label="Sensor Name" width="150"></el-table-column>
      <el-table-column prop="sensor_device" label="Sensor Device" width="150"></el-table-column>
      <el-table-column prop="sensor_type" label="Sensor Type" width="150"></el-table-column>
      <el-table-column prop="sensor_agent" label="Sensor Agent" width="150"></el-table-column>

    </el-table>
  </el-scrollbar>

</el-container>
</template>

<script>

export default {
  data() {
    return {
      sensors: [],
      loading: false,
      elTableHeight: $('.el-scrollbar').height(),
    }
  },
  created() {
    // this.loading = true
    window.addEventListener('resize', this.handelHeighChange)
  },
  destroyed() {
    window.removeEventListener('resize', this.handelHeighChange)
  },
  methods: {
    handelHeighChange() {
      this.elTableHeight = $('.el-scrollbar').height()
    }
  }
}
</script>

<style scoped>

</style>