<script setup>

</script>

<template>
<h1>Agent Generator</h1>

<!--  <el-form ref="generator-form" :model="form" label-width="100px">-->
<!--    <el-form-item label="agent_id">-->
<!--      // TODO: finish the form-->
<!--    </el-form-item>-->
<!--  </el-form>-->

  <div class="agent-generator">
    <el-input
      type="textarea"
      v-model="description"
      placeholder="Type the description of the sensor agent here"
      rows="5"
      :autosize="{ minRows: 5, maxRows: 10 }"
    ></el-input>

    <el-button type="primary" style="margin-top: 10px;" @click="generateAgentCode">Generate</el-button>

    <div v-if="agentCode">
      <h3>Generated Agent Code</h3>
      <pre v-html="highlightedCode" class="hljs"></pre>
      <el-button @click="saveCode" style="margin-top: 10px; " >Save Code</el-button>
    </div>
    </div>
</template>

<script>
import hljs from 'highlight.js/lib/core';
import python from 'highlight.js/lib/languages/python';
hljs.registerLanguage('python', python);

export default {
  data() {
    return {
      description: '',  // 用户输入的描述
      agentCode: '',    // 生成的代码
    };
  },
  computed: {
    // 返回高亮后的代码
    highlightedCode() {
      return hljs.highlight(this.agentCode, { language: 'python' }).value;
    },
  },
  methods: {
    // 模拟代码生成逻辑
    generateAgentCode() {
      if (this.description) {
        // 实际上可以调用 API 生成代码
        this.agentCode = `def agent():\n    # Based on description\n    description = "${this.description}"\n    print("Agent created")`;
      }
    },
    // 保存代码到本地
    saveCode() {
      const blob = new Blob([this.agentCode], { type: 'text/plain;charset=utf-8' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'tmp_agent.py';  // 文件名
      link.click();
      URL.revokeObjectURL(link.href);
    },
  },
};
</script>

<style>
.agent-generator {
  max-width: 600px;
  margin: 0 auto;
}
pre {
  background-color: #f5f5f5;
  padding: 15px;
  border-radius: 5px;
}
</style>
