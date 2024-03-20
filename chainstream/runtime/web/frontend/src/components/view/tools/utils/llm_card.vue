<script setup>
defineProps({
  model_name: {
    type: String,
    default: 'LLM Card',
    required: true
  }
})
</script>

<template>
  <el-card style="max-width: 480px" shadow="hover">
    <template #header>
      <div class="card-header">
        <span> {{ model_name }} </span>
      </div>
    </template>

<!--      <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>-->
    <el-container >
    <el-row style="width: 100%;">
      <el-col v-for="(item, index) in statisticalData" :span="24" style="align-content: center; justify-content: center; text-align: center;" >
        <el-statistic :title=item.title :value=item.value />
      </el-col>
    </el-row>
      </el-container>
    <template #footer>
      <el-row justify="end">
        <el-button type="primary" size="default">
          <el-icon><RefreshRight/></el-icon> Refresh
        </el-button>
        <el-button type="primary" size="default" @click="drawer2 = true">More</el-button>
      </el-row>
    </template>
  </el-card>

  <el-drawer v-model="drawer2" :direction="direction">
    <template #header>
      <h4>set title by slot</h4>
    </template>
    <template #default>
      <div>
        <el-radio v-model="radio1" value="Option 1" size="large"
        >Option 1</el-radio
        >
        <el-radio v-model="radio1" value="Option 2" size="large"
        >Option 2</el-radio
        >
      </div>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="cancelClick">cancel</el-button>
        <el-button type="primary" @click="confirmClick">confirm</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<script>

export default {
  data() {
    return {
      statisticalData: [
          { title: 'Total Usage', value: 268500 },
          { title: 'Agent Count', value: 100 },
          { title: 'User Count', value: 1000 },
          { title: 'Device Count', value: 10000 },
      ]

    }
  }
}

</script>

<style scoped>

.el-card {
  margin: 10px;
  padding: 10px;
  width: 50vh;
  height: 20lh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-header {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

</style>