<script setup>

</script>

<template>
  <h1>Welcome to ChainStream Runtime!</h1>
  <h2>ChainStream Configuration</h2>
  <div style="margin-top: 50px; width: 50%;">
    <el-descriptions
      title=""
      column="3"
      size="small"
      border
      direction="vertical"
      v-loading="loading"
  >

    <el-descriptions-item label="Backend URL">
      {{ backendUrl }}
    </el-descriptions-item>
    <el-descriptions-item align="center">
      <template #default>
        <el-button size="small" type="success" @click="checkConn()">Test Connection</el-button>
      </template>
    </el-descriptions-item>


  </el-descriptions>
  </div>
</template>

<script>
import { reactive } from 'vue'
import { checkConnection } from '@/api/home.js'
import axios from "axios";

export default {
  name: 'Home',
  setup() {
    const formInline = reactive({
      backendUrl: "hh",

    })

    const handleSubmit = () => {
      console.log(formInline.name)
    }

    return {
      formInline,
      handleSubmit
    }
  },
  data() {
    return {
      backendUrl: import.meta.env.VITE_CHAINSTREAM_BACKEND_API ,
      loading: false
    }
  },
  methods: {
    checkConn(onfulfilled) {
      this.loading = true
        checkConnection()
            .then(res => {
              this.loading = false
              console.log(res)
              this.$message.success('Connection successful')
            }, err => {
              this.loading = false
              console.log(err)
              this.$message.error('Connection failed')
            }, 10000)

      // axios.get('/api/home/checkConnection')
      //     .then(res => {
      //       this.loading = false
      //       console.log(res)
      //       this.$message.success('Connection successful')
      //     }).catch(err => {
      //   this.loading = false
      //   console.log(err)
      //   this.$message.error('Connection failed')
      // })
    }
  }
}

</script>


<style scoped>
  h1 {
    color: #3b86d0;
    font-size: 36px;
    font-weight: bold;
    //margin-top: 50px;
  }
  h2 {
    color: #3b86d0;
    font-size: 24px;
    font-weight: bold;
  }
</style>