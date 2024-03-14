<script setup>

</script>

<template>
  <el-scrollbar>
    <el-table :data="agents" style="width: 100%">
      <el-table-column prop="path" label="Path" width="180">
      </el-table-column>
      <el-table-column prop="name" label="Name" width="180">
      </el-table-column>
      <el-table-column prop="status" label="Status" width="120">
      </el-table-column>
      <el-table-column prop="version" label="Version" width="120">
      </el-table-column>
      <el-table-column prop="last_seen" label="Last Seen" width="180">
      </el-table-column>
    </el-table>
  </el-scrollbar>
</template>

<style scoped>

</style>