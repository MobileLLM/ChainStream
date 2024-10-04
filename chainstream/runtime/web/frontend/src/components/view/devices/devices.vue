<!--<script setup>-->
<!--import device_card from "@/components/view/devices/utils/device_card.vue"-->
<!--</script>-->

<!--<template>-->
<!--  <el-row style="height: auto;">-->
<!--    <el-col :span="12">-->
<!--      <el-text style="font-size: 24px; text-align: center; font-weight: bold" type="primary">Devices</el-text>-->
<!--    </el-col>-->
<!--    <el-col :span="12" style="display: flex; justify-content: flex-end; text-align: right">-->
<!--      <el-button type="primary" style="float: right; margin-top: 10px" @click="showAddDeviceDialog = true">+ Add Device</el-button>-->
<!--    </el-col>-->
<!--  </el-row>-->

<!--  &lt;!&ndash; 弹窗部分 &ndash;&gt;-->
<!--  <el-dialog title="Add Device" :visible.sync="showAddDeviceDialog" width="30%" @close="handleClose">-->
<!--    <el-form :model="deviceForm" label-width="120px">-->
<!--      &lt;!&ndash; 设备名称 &ndash;&gt;-->
<!--      <el-form-item label="Device Name">-->
<!--        <el-input v-model="deviceForm.name" placeholder="Enter device name"></el-input>-->
<!--      </el-form-item>-->

<!--      &lt;!&ndash; IP地址 &ndash;&gt;-->
<!--      <el-form-item label="IP Address">-->
<!--        <el-input v-model="deviceForm.ip" placeholder="Enter IP address"></el-input>-->
<!--      </el-form-item>-->

<!--      &lt;!&ndash; 种类 &ndash;&gt;-->
<!--      <el-form-item label="Type">-->
<!--        <el-select v-model="deviceForm.type" placeholder="Select device type">-->
<!--          <el-option label="Phone" value="Phone"></el-option>-->
<!--          <el-option label="Watch" value="Watch"></el-option>-->
<!--          <el-option label="ChainStreamSensor" value="ChainStreamSensor"></el-option>-->
<!--        </el-select>-->
<!--      </el-form-item>-->
<!--    </el-form>-->

<!--    &lt;!&ndash; 底部操作按钮 &ndash;&gt;-->
<!--    <span slot="footer" class="dialog-footer">-->
<!--      <el-button @click="showAddDeviceDialog = false">Cancel</el-button>-->
<!--      <el-button type="primary" @click="submitForm">Confirm</el-button>-->
<!--    </span>-->
<!--  </el-dialog>-->


<!--  <el-container>-->
<!--    <el-row style=" width: 100%; margin: 0; padding: 0" align="middle" justify="start">-->
<!--      &lt;!&ndash; 使用v-for循环遍历cards数组 &ndash;&gt;-->
<!--      <el-col v-for="(card, index) in cards" :key="index" :span="6" style="align-content: center; justify-content: center;">-->
<!--        <device_card :model_name="card.model_name"></device_card>-->
<!--      </el-col>-->
<!--    </el-row>-->
<!--  </el-container>-->

<!--</template>-->

<!--<script>-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      cards: [-->
<!--        { model_name: "Phone", content: 'Content of card'},-->
<!--        { model_name: "Watch", content: 'Content of card'},-->
<!--        { model_name: "ChainStreamSensor", content: 'Content of card'}-->
<!--      ],-->

<!--      // 表单数据-->
<!--      deviceForm: {-->
<!--        name: '',-->
<!--        ip: '',-->
<!--        type: ''-->
<!--      }-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    submitForm() {-->
<!--      this.$refs.deviceForm.validate((valid) => {-->
<!--        if (valid) {-->
<!--          // 提交数据逻辑，例如保存到数据库或其他处理-->
<!--          console.log('Submitted device:', this.deviceForm);-->

<!--          // 提交后关闭弹窗-->
<!--          this.showAddDeviceDialog = false;-->

<!--          // 清空表单数据-->
<!--          this.resetForm();-->
<!--        } else {-->
<!--          console.log('Form validation failed');-->
<!--          return false;-->
<!--        }-->
<!--      });-->
<!--    },-->

<!--    // 重置表单-->
<!--    resetForm() {-->
<!--      this.deviceForm = {-->
<!--        name: '',-->
<!--        ip: '',-->
<!--        type: ''-->
<!--      };-->
<!--    },-->

<!--    // 关闭弹窗时重置表单-->
<!--    handleClose() {-->
<!--      this.resetForm();-->
<!--    }-->
<!--  }-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->

<!--</style>-->

<template>

  <el-row style="height: auto;">
    <el-col :span="12">
      <el-text style="font-size: 24px; text-align: center; font-weight: bold" type="primary">Devices</el-text>
    </el-col>
    <el-col :span="12" style="display: flex; justify-content: flex-end; text-align: right">
      <el-button type="primary" style="float: right; margin-top: 10px" @click="dialogFormVisible = true">+ Add Device</el-button>
    </el-col>
  </el-row>

  <el-dialog v-model="dialogFormVisible" title="Add New Device" width="500">
    <el-form :model="deviceForm">
      <el-form-item label="Device name" :label-width="formLabelWidth">
        <el-input v-model="deviceForm.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="IP address" :label-width="formLabelWidth">
        <el-input v-model="deviceForm.ip" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Device type" :label-width="formLabelWidth">
        <el-select v-model="deviceForm.type" placeholder="Please select a device type">
          <el-option label="Android device" value="android" />
          <el-option label="Linux device" value="linux" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Cancel</el-button>
        <el-button type="primary" @click="dialogFormVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-container>
    <el-row style=" width: 100%; margin: 0; padding: 0" align="middle" justify="start">
      <!-- 使用v-for循环遍历cards数组 -->
      <el-col v-for="(card, index) in cards" :key="index" :span="6" style="align-content: center; justify-content: center;">
        <device_card :model_name="card.model_name"></device_card>
      </el-col>
    </el-row>
  </el-container>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import device_card from "@/components/view/devices/utils/device_card.vue"

const dialogTableVisible = ref(false)
const dialogFormVisible = ref(false)
const formLabelWidth = '140px'

const deviceForm = reactive({
  name: '',
  ip: '',
  type: '',
})

const cards = [
  { model_name: "Phone", content: 'Content of card'},
  { model_name: "Watch", content: 'Content of card'},
  { model_name: "Edge Sensor", content: 'Content of card'}
]

</script>
