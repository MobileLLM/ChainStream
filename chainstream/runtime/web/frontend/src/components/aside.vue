<script setup>

import {Edit, Message, Setting} from "@element-plus/icons-vue";
</script>

<template>
  <el-scrollbar style="height: calc(100% - 60px);">
    <el-menu  active-text-color="#165CCAFF" router>
      <el-menu-item index="/home"><el-icon><home /></el-icon>Home</el-menu-item>
      <el-sub-menu index="1">
        <template #title>
          <el-icon><edit /></el-icon>Runtime Config
        </template>
        <el-menu-item index="">Stream Graph(尚未开发)</el-menu-item>
        <el-menu-item index="">Agents(尚未开发)</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="2">
        <template #title>
          <el-icon><monitor /></el-icon>Runtime Monitor
        </template>
        <el-menu-item index="/monitor/Streams">Streams</el-menu-item>
        <el-menu-item index="/monitor/Agents">Agents</el-menu-item>
        <el-menu-item index="/monitor/StreamGraph">Stream Graph</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="3">
        <template #title>
          <el-icon><Memo /></el-icon>Memory
        </template>
        <el-menu-item index="/memory/Memory">Memroy</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="4">
        <template #title>
          <el-icon><Brush /></el-icon>Tools
        </template>

        <el-menu-item index="/tools/llms">LLMs</el-menu-item>
        <el-menu-item index="/tools/tools">Tools</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="5">
        <template #title>
          <el-icon><DataLine /></el-icon>Analysis
        </template>
        <el-menu-item index="/analysis/analysis">Analysis(尚未开发)</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="6">
        <template #title>
          <el-icon><Iphone /></el-icon>Devices
        </template>
        <el-menu-item index="/device/device">Devices</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="7">
        <template #title>
          <el-icon><ShoppingTrolley /></el-icon>Agent Store
        </template>
        <el-menu-item index="/store/store">Agent Store</el-menu-item>
      </el-sub-menu>

      <el-sub-menu index="8">
        <template #title>
          <el-icon><setting /></el-icon>Settings
        </template>
        <el-menu-item index="">Stream Graph(尚未开发)</el-menu-item>
        <el-menu-item index="">Agents(尚未开发)</el-menu-item>
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