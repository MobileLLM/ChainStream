<script setup>
import { 
  Edit, 
  HomeFilled, 
  Message, 
  Setting, 
  TopLeft,
  House,
  Iphone,
  ShoppingTrolley,
  Monitor,
  Memo,
  DataLine,
  Share
} from "@element-plus/icons-vue";
import { defineProps } from 'vue';

const props = defineProps({
  user: {
    type: Object,
    default: null
  }
});
</script>

<template>
  <div class="aside-container">
    <el-scrollbar class="menu-scrollbar">
      <el-menu 
        class="sidebar-menu"
        active-text-color="#409EFF" 
        text-color="#ffffff"
        background-color="transparent"
        router
      >
        <el-menu-item index="/home" class="menu-item">
          <el-icon><House /></el-icon>
          <span class="menu-text">{{ $t('menu.home') }}</span>
        </el-menu-item>
        
<!--        <el-sub-menu index="1" class="sub-menu">-->
<!--          <template #title>-->
<!--            <el-icon><Setting /></el-icon>-->
<!--            <span class="menu-text">{{ $t('menu.systemConfig') }}</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/config/llms" class="sub-menu-item">{{ $t('menu.llms') }}</el-menu-item>-->
<!--          <el-menu-item index="/config/tools" class="sub-menu-item">{{ $t('menu.tools') }}</el-menu-item>-->
<!--        </el-sub-menu>-->

<!--        <el-sub-menu index="2" class="sub-menu">-->
<!--          <template #title>-->
<!--            <el-icon><Iphone /></el-icon>-->
<!--            <span class="menu-text">{{ $t('menu.devices') }}</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/device/device" class="sub-menu-item">{{ $t('menu.device') }}</el-menu-item>-->
<!--          <el-menu-item index="/device/sensor" class="sub-menu-item">{{ $t('menu.sensor') }}</el-menu-item>-->
<!--        </el-sub-menu>-->

<!--        <el-sub-menu index="3" class="sub-menu">-->
<!--          <template #title>-->
<!--            <el-icon><ShoppingTrolley /></el-icon>-->
<!--            <span class="menu-text">{{ $t('menu.agentStore') }}</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/store/store" class="sub-menu-item">{{ $t('menu.store') }}</el-menu-item>-->
<!--        </el-sub-menu>-->

        <el-sub-menu index="4" class="sub-menu">
          <template #title>
            <el-icon><Edit /></el-icon>
            <span class="menu-text">{{ $t('menu.agentGenerator') }}</span>
          </template>
          <el-menu-item index="/generator/Generator" class="sub-menu-item">{{ $t('menu.generator') }}</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="5" class="sub-menu">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span class="menu-text">{{ $t('menu.runtimeMonitor') }}</span>
          </template>
          <el-menu-item index="/monitor/Agents" class="sub-menu-item">{{ $t('menu.agents') }}</el-menu-item>
          <el-menu-item index="/monitor/Streams" class="sub-menu-item">{{ $t('menu.streams') }}</el-menu-item>
          <el-menu-item index="/monitor/StreamGraph" class="sub-menu-item">{{ $t('menu.streamGraph') }}</el-menu-item>
        </el-sub-menu>

<!--        <el-sub-menu index="6" class="sub-menu">-->
<!--          <template #title>-->
<!--            <el-icon><Memo /></el-icon>-->
<!--            <span class="menu-text">{{ $t('menu.memory') }}</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/memory/Memory" class="sub-menu-item">{{ $t('menu.memory') }}</el-menu-item>-->
<!--        </el-sub-menu>-->

<!--        <el-sub-menu index="7" class="sub-menu">-->
<!--          <template #title>-->
<!--            <el-icon><DataLine /></el-icon>-->
<!--            <span class="menu-text">{{ $t('menu.analysis') }}</span>-->
<!--          </template>-->
<!--          <el-menu-item index="/analysis/analysis" class="sub-menu-item">{{ $t('menu.analysis') }}</el-menu-item>-->
<!--        </el-sub-menu>-->
      </el-menu>
    </el-scrollbar>
    
    <!-- <div class="aside-footer">
      <div class="footer-content">
        <el-icon class="footer-icon"><Share /></el-icon>
        <span class="footer-text">ChainStream ©2024</span>
      </div>
    </div> -->
  </div>
</template>

<style lang="scss" scoped>
.aside-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: transparent;
}

.menu-scrollbar {
  flex: 1;
  height: calc(100% - 60px);
}

.sidebar-menu {
  border: none;
  background: transparent;
  
  :deep(.el-menu-item) {
    color: #ffffff;
    background: transparent;
    border-radius: 8px;
    margin: 4px 12px;
    transition: all 0.3s ease;
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #409EFF;
    }
    
    &.is-active {
      background: rgba(64, 158, 255, 0.2);
      color: #409EFF;
      border-right: 3px solid #409EFF;
    }
  }
  
  :deep(.el-sub-menu) {
    .el-sub-menu__title {
      color: #ffffff;
      background: transparent;
      border-radius: 8px;
      margin: 4px 12px;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #409EFF;
      }
    }
    
    .el-menu {
      background: rgba(0, 0, 0, 0.2);
      border-radius: 8px;
      margin: 0 8px;
      
      .el-menu-item {
        color: #e0e0e0;
        margin: 2px 8px;
        padding-left: 40px !important;
        
        &:hover {
          background: rgba(255, 255, 255, 0.1);
          color: #409EFF;
        }
        
        &.is-active {
          background: rgba(64, 158, 255, 0.2);
          color: #409EFF;
        }
      }
    }
  }
}

.menu-item,
.sub-menu {
  .menu-text {
    margin-left: 8px;
    font-weight: 500;
  }
}

.sub-menu-item {
  font-size: 0.9rem;
}

.aside-footer {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 60, 144, 0.8);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-content {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #f3e7e7;
}

.footer-icon {
  font-size: 16px;
}

.footer-text {
  font-size: 14px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .menu-scrollbar {
    height: calc(100% - 50px);
  }
  
  .aside-footer {
    height: 50px;
  }
  
  .sidebar-menu {
    :deep(.el-menu-item),
    :deep(.el-sub-menu .el-sub-menu__title) {
      margin: 2px 8px;
      font-size: 0.9rem;
    }
  }
  
  .footer-text {
    font-size: 12px;
  }
}

@media (max-width: 480px) {
  .sidebar-menu {
    :deep(.el-menu-item),
    :deep(.el-sub-menu .el-sub-menu__title) {
      margin: 1px 4px;
      font-size: 0.85rem;
    }
    
    :deep(.el-sub-menu .el-menu .el-menu-item) {
      padding-left: 30px !important;
      font-size: 0.8rem;
    }
  }
}
</style>