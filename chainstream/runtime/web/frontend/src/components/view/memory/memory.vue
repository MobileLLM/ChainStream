<script setup>
import $ from 'jquery'
</script>

<template>
<el-container style="height: 100%; margin: 0; padding: 0;">
  <el-scrollbar>
    <el-table :height="elTableHeight" v-loading="loading" :data="memoryData" style="width: 100%;" table-layout="auto">
      <el-table-column type="index" label="#" width="100"></el-table-column>
      <el-table-column prop="memory_id" label="Memory ID" width="150"></el-table-column>
      <el-table-column prop="memory_name" label="Memory Name" width="150"></el-table-column>
      <el-table-column prop="memory_size" label="Memory Size" width="150"></el-table-column>
      <el-table-column prop="memory_type" label="Memory Type" width="150"></el-table-column>
      <el-table-column prop="create_agent" label="Create Agent" width="150"></el-table-column>

    </el-table>
  </el-scrollbar>

</el-container>
</template>

<script>

export default {
  data() {
    return {
      memoryData: [],
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