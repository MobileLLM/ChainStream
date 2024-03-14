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
  >

    <el-descriptions-item label="Backend URL">
      {{ this.$BACKEND_URL }}
    </el-descriptions-item>


  </el-descriptions>
  </div>
</template>

<script>
import { reactive } from 'vue'

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