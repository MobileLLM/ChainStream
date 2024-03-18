<script setup>
import $ from 'jquery';
</script>

<template>
<el-container style="height: 100%; margin: 0; padding: 0;">
  <el-scrollbar>
    <el-table :height="elTableHeight" v-loading="loading" :data="streams" style="width: 100%;" table-layout="auto">
      <el-table-column type="index" label="#" width="100"></el-table-column>
      <el-table-column prop="stream_id" label="stream_id" width="150"></el-table-column>
      <el-table-column prop="type" label="类型" width="100"></el-table-column>
      <el-table-column prop="status" label="状态" width="100"></el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="200"></el-table-column>
      <el-table-column prop="created_by" label="创建者" width="200"></el-table-column>
      <el-table-column prop="listen_agnet" label="监听者" width="200"></el-table-column>

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
        this.streams = res.data;
        this.$message.success("获取流信息成功");
        this.loading = false;
      }).catch(err => {
        console.log(err);
        this.$message.error("获取流信息失败");
        this.loading = false;
      });
    },
    handleHightChange() {
      this.elTableHeight = $('.el-scrollbar').height();
    }
  },
  // mounted() {
  //   this.elTableHeight = $('.el-scrollbar').height();
  // }
}
</script>

<style scoped>

</style>