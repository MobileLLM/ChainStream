<script setup>
import llm_card from "@/components/view/tools/utils/llm_card.vue";
</script>

<template>
<el-text style="font-size: 24px; text-align: center; margin-top: 50px; font-weight: bold" type="primary">LLMS</el-text>
  <el-container>
    <el-row style="height: 40vh; width: 100%; margin: 0; padding: 0" align="middle" justify="start">
      <!-- 使用v-for循环遍历cards数组 -->
      <el-col v-for="(card, index) in cards" :key="index" :span="6" style="align-content: center; justify-content: center;">
        <llm_card :model_name="card.model_name"></llm_card>
      </el-col>
    </el-row>

  </el-container>
</template>

<script>
export default {
  data() {
    return {
      cards: [ // 你的卡片数据数组=
        { model_name: "GPT3.5", content: 'Content of card'},
        { model_name: "GPT3.5", content: 'Content of card'},
        { model_name: "GPT3.5", content: 'Content of card'}
      ]
    };
  }
};
</script>

<style scoped>

</style>