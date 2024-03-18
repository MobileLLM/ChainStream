<template>
  <el-row>
    <el-col class="chainstream" :span="6" style="text-align: center; background-color: #ab2222; justify-content: center;">
      <h1 style="color: white;">ChainStream Runtime</h1>
    </el-col>
    <el-col class="menu" :span="18" style="text-align: right; background-color: #d71111; justify-content: right;">
      <span style="align-self: center;">
<!--        <el-icon class="el-icon&#45;&#45;right" style="margin-right: 1px; font-size: 10px; color: white;"><arrow-down /></el-icon>-->
<!--        <el-icon style="margin-right: 10px; font-size: 30px; color: white;"><setting /></el-icon>-->
      </span>
      <el-dropdown >
        <el-icon style="margin-right: 10px; font-size: 30px; color: white;"><setting /></el-icon>
        <template v-slot:dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>View</el-dropdown-item>
            <el-dropdown-item>Add</el-dropdown-item>
            <el-dropdown-item>Delete</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-col>

  </el-row>
</template>

<style lang="scss">
.el-row {
  height: 100%;
  align-items: center;
}

.el-col {
  height: 100%;
  display: flex;
  align-items: center;
  //justify-content: center;
  padding: 0;
  margin: 0;
}

#chainstream {
  height: 100%;
  text-align: center;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
}

#menu {
  height: 100%;
  text-align: right;
  //display: inline-flex;
  align-items: center;
  justify-content: right;
  padding: 0;
  margin: 0;
}

h1 {
  font-size: 140%;
  margin: 0;
  font-weight: bold;
  padding: 0;
}


</style>
<script setup>
</script>