<template>

  <el-row style="height: auto;">
    <el-col :span="12">
      <el-text style="font-size: 24px; text-align: center; font-weight: bold" type="primary">Devices</el-text>
    </el-col>

    <el-col :span="12" style="display: flex; justify-content: flex-end; text-align: right">
<!--      <el-button type="primary" @click="fetchDeviceCards()">Refresh</el-button>-->
      <el-button type="primary" style="float: right; margin-top: 10px" @click="dialogFormVisible = true">+ Add Device</el-button>
    </el-col>
  </el-row>


  <el-dialog v-model="dialogFormVisible" title="Add New Device" width="800" @close="resetForm()">

<!--    <el-text size="large">Device base information</el-text>-->
    <h2>Device base information</h2>

    <el-form :model="deviceForm" label-position="right">
      <el-form-item label="Device name" :label-width="formLabelWidth">
        <el-input v-model="deviceForm.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Device type" :label-width="formLabelWidth">
        <el-select v-model="deviceForm.type" placeholder="Please select a device type">
          <el-option label="Android device" value="android" />
          <el-option label="Linux device" value="linux" />
        </el-select>
      </el-form-item>
      <el-form-item label="IP address" :label-width="formLabelWidth">
        <el-input v-model="deviceForm.ip" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Port" :label-width="formLabelWidth">
        <el-input v-model="deviceForm.port" autocomplete="off" />
      </el-form-item>
    </el-form>

    <h2 v-if="isNewDeviceChecked">Sensor information</h2>
    <el-form v-if="isNewDeviceChecked" v-for="(sensor, index) in sensorForm" :key="index" :model="sensor">
      <h3>Sensor {{ index }}</h3>
      <el-form-item :label="'Name ' + index" size="small">
        <el-input v-model="sensor.name" autocomplete="off" />
      </el-form-item>
<!--      <el-form-item label="Device type">-->
<!--        <el-select v-model="sensor.type" placeholder="Please select a device type">-->
<!--          <el-option label="Android device" value="android" />-->
<!--          <el-option label="Linux device" value="linux" />-->
<!--        </el-select>-->
<!--      </el-form-item>-->
      <el-form-item :label="'Type ' + index" size="small">
        <el-input v-model="sensor.type" autocomplete="off" />
      </el-form-item>
<!--      <el-form-item label="Agent">-->
<!--        <el-input v-model="sensor.agent" autocomplete="off" />-->
<!--      </el-form-item>-->
      <el-form-item :label="'Agent ' + index" size="small">
        <el-select v-model="sensor.agent" placeholder="Select">
<!--          <el-option label="Android device" value="android" />-->
<!--          <el-option label="Linux device" value="linux" />-->
          <el-option v-for="(agent, index) in agent_list" :key="index" :label="agent.label" :value="agent.value"></el-option>
        </el-select>
<!--        <el-cascader-->
<!--          v-model="agent_list"-->
<!--          :options="agent_list"-->
<!--          :props="props"-->
<!--          @change="handleChange"-->
<!--          clearable-->
<!--        />-->
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false; resetForm()">Cancel</el-button>
        <el-button v-if="isNewDeviceChecked" type="success" @click="dialogFormVisible = false">
          Add New Device
        </el-button>
        <el-button v-else type="primary" @click="isNewDeviceChecked = true">
          Check
        </el-button>
      </div>
    </template>
  </el-dialog>

  <el-container v-loading="isLoading">
  <el-row style="width: 100%;" align="middle" justify="start">
    <el-col v-for="(card, index) in device_cards" :key="index" :span="6">
      <device_card :model_name="card.model_name"></device_card>
    </el-col>
  </el-row>
  </el-container>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted } from 'vue'
import device_card from '@/components/view/devices/utils/device_card.vue'
import { getDeviceCards, getAgentList, checkDevice, addDevice} from "@/api/devices/devices.js"

const dialogFormVisible = ref(false)

const isNewDeviceChecked = ref(false)

const formLabelWidth = '140px'

const isLoading = ref(true)

const deviceForm = reactive({
  name: '',
  ip: '',
  port: '',
  type: '',
})

const sensorForm = reactive([
    {
      name: '',
      type: '',
      agent: '',
    },
    {
      name: '',
      type: '',
      agent: '',
    },
])

const device_cards = reactive([])

const agent_list = reactive([
  {
    value: 'agent1',
    label: 'Agent 1',},
    {
    value: 'agent2',
    label: 'Agent 2',},
    {
    value: 'agent3',
    label: 'Agent 3',},
])

const resetForm = () => {
  deviceForm.name = ''
  deviceForm.ip = ''
  deviceForm.type = ''
  isNewDeviceChecked.value = false
  // sensorForm.clear()
}

const fetchAgentList = () => {
  try {
    getAgentList().then(response => {
      agent_list.length = 0
      agent_list.push(...response.data)
    })
  } catch (error) {
    console.error('Failed to fetch agents:', error)
  }
}

const fetchDeviceCards = async () => {
  try {
    isLoading.value = true
    const response = await getDeviceCards()
    // console.log(JSON.stringify(response.data))
    device_cards.splice(0, device_cards.length, ...response.data)
    console.log("   device_cards:")
    console.log(device_cards)
  } catch (error) {
    console.error('Failed to fetch device cards:', error)
  } finally {
    isLoading.value = false
  }
}

const checkDeviceForm = () => {
  try {
    checkDevice(deviceForm).then(response => {
      sensorForm.length = 0
      sensorForm.push(...response.data)
      isNewDeviceChecked.value = true
    })
  } catch (error) {
    console.error('Failed to add device:', error)
  }
}

const addNewDevice = () => {
  try {
    const payload = {
      device_form: deviceForm,
      sensor_form: sensorForm,
    }
    addDevice(payload).then(response => {
      console.log('New device added:', response.data)

      dialogFormVisible.value = false
      resetForm()
      fetchDeviceCards()
    })
  } catch (error) {
    console.error('Failed to add device:', error)
  }
}

// 在页面加载时获取代理列表和设备卡片
onMounted(() => {
  fetchAgentList()
  fetchDeviceCards()
})

</script>
