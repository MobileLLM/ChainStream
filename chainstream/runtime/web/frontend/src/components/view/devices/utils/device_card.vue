<script setup>
import { ref } from 'vue';
// import {, MoreFilled, TurnOff} from "@element-plus/icons-vue";
import {
    RefreshRight,
    Delete,
    MoreFilled,
    TurnOff,
    Open,
    Edit,
} from '@element-plus/icons-vue'

const isOn = ref(false);
const togglePower = () => {
  isOn.value = !isOn.value;  // 切换状态
};

defineProps({
  model_name: {
    type: String,
    default: 'LLM Card',
    required: true
  }
})
</script>

<template>
  <el-card shadow="hover" style="max-width: 480px;">
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
      <div class="card-footer">
      <el-row justify="center">

        <el-col :span="6">
<!--          <el-button size="default" @click=""><el-icon><TurnOff/></el-icon></el-button>-->
<!--          <el-button :icon="Open" circle></el-button>-->
<!--          <el-button size="default" :type="isOn ? 'success' : 'info'" @click="togglePower" round>-->
<!--            <el-icon>-->
<!--              &lt;!&ndash; 根据isOn状态显示不同图标 &ndash;&gt;-->
<!--              <component :is="isOn ? Open : TurnOff" />-->
<!--            </el-icon>-->
<!--          </el-button>-->
<!--          <el-switch v-model="isOn" active-color="#13ce66" inactive-color="#ff4949" />-->

          <el-switch
            v-model="isOn"></el-switch>

<!--          <el-switch-->
<!--            v-model="isOn"-->
<!--            class="ml-2"-->
<!--            style="&#45;&#45;el-switch-on-color: #13ce66; &#45;&#45;el-switch-off-color: #ff4949"-->
<!--          />-->

        </el-col>

        <el-col :span="4" justify="left">
<!--          <el-button size="default" type="text">-->
<!--            <el-icon><RefreshRight/></el-icon>-->
<!--          </el-button>-->
          <el-button  :icon="RefreshRight" circle />
        </el-col>



        <el-col :span="4">
<!--          <el-button size="default" type="danger" @click=""><el-icon><Delete/></el-icon></el-button>-->
          <el-button type="danger" :icon="Delete" circle />
        </el-col>

        <el-col :span="4">
<!--          <el-button size="default" type="danger" @click=""><el-icon><Delete/></el-icon></el-button>-->
          <el-button type="warning" :icon="Edit" circle />
        </el-col>

        <el-col :span="4">
          <el-button size="default" type="primary" :icon="MoreFilled" @click="drawer2 = true" circle></el-button>
        </el-col>

      </el-row>
<!--      <el-row justify="center">-->
<!--          <el-button size="small" type="primary" @click="drawer2 = true">More</el-button>-->
<!--      </el-row>-->
        </div>
    </template>
  </el-card>

  <el-drawer v-model="drawer2" direction="rtl">
    <template #header>
      <h1>{{ model_name }}</h1>
    </template>
    <template #default>

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
      ],
      drawer2: false

    }
  },
  methods: {
    cancelClick() {
      this.drawer2 = false;
    },
    confirmClick() {
      this.drawer2 = false;
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