<script setup>
import llm_card from "@/components/view/store/utils/agent_card.vue";
</script>

<template>
<el-text style="font-size: 24px; text-align: center; margin-top: 50px; font-weight: bold" type="primary">Agents</el-text>
  <el-container>
    <el-row style="width: 100%; margin: 0; padding: 0" align="middle" justify="start">
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
      cards: [
        { model_name: "Desktop", content: 'Content of card'},
        { model_name: "MeetingRoom", content: 'Content of card'},
        { model_name: "Wearable", content: 'Content of card'}
      ]
    };
  }
};
</script>

<style scoped>

</style>