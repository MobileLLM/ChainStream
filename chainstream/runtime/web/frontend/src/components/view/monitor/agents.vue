<script setup>

</script>


<template>
  <el-container style="height: 100%; margin: 0; padding: 0">
    <el-scrollbar>
      <el-table :data="agents" style="width: 100%;">
        <el-table-column prop="path" label="Agent ID" width="180">
        </el-table-column>
        <el-table-column prop="name" label="Description" width="180">
        </el-table-column>
        <el-table-column prop="status" label="Status" width="120">
        </el-table-column>
        <el-table-column prop="version" label="Version" width="120">
        </el-table-column>
        <el-table-column prop="last_seen" label="Last Seen" width="180">
        </el-table-column>
      </el-table>
    </el-scrollbar>
  </el-container>
</template>


<script>

export  default {
  data() {
    return {
      agents: [
        {
          "Agent ID": "haha",
          "Description" : "lala",
          "Status": "xixi",
          "Version": "1",
          "Last Seen": "zizi"
        }
      ]
    }
  },
}
</script>

<style scoped>

</style>