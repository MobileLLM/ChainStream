<script setup>
import Header from './components/header.vue'
import Aside from './components/aside.vue'
</script>

<template>
    <el-container style="height: 100%; width: 100%; margin: 0; padding: 0;">
      <el-header style="padding: 0; margin: 0; border: none; height: 60px;">
        <Header />
      </el-header>

      <el-container style="height: calc(100% - 60px); width: 100%; margin: 0; padding: 0;">
        <el-aside width="300px" style="background-color: #165cca;">
          <Aside />
        </el-aside>
        <el-main style="background-color: #d7ad21;">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>

</template>

<script>


</script>

<style>
el-container, el-header, el-aside, el-main {
  padding: 0;
  margin: 0;
}
el-container {
  width: 100%;
  height: 100%;
}

el-aside {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>

