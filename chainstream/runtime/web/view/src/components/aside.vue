<script setup>

import {Edit, Message, Setting} from "@element-plus/icons-vue";
</script>

<template>
  <el-scrollbar style="height: calc(100% - 60px);">
    <el-menu >
      <el-sub-menu index="1">
        <template #title>
          <el-icon><edit /></el-icon>Runtime Config
        </template>
        <el-menu-item index="">Stream Graph</el-menu-item>
        <el-menu-item index="">Agents</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="2">
        <template #title>
          <el-icon><monitor /></el-icon>Runtime Monitor
        </template>
        <el-menu-item index="">Stream Graph</el-menu-item>
        <el-menu-item index="">Agents</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="3">
        <template #title>
          <el-icon><setting /></el-icon>Settings
        </template>
        <el-menu-item index="">Stream Graph</el-menu-item>
        <el-menu-item index="">Agents</el-menu-item>
      </el-sub-menu>



    </el-menu>
  </el-scrollbar>
  <el-footer style="height: 60px; display: flex; align-items: center; justify-content: center; background-color: #0f3c90;">
    <el-space direction="vertical" style="align-items: center; justify-content: center;">
      <el-text style="font-size: 16px; color: #f3e7e7;">
        <el-icon><share /></el-icon>
        ChainStream ©2024
      </el-text>
    </el-space>
  </el-footer>
</template>

<style scoped>

</style>