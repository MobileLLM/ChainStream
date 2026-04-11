<template>
  <el-dialog
    v-model="visible"
    :title="title"
    width="80%"
    :before-close="handleClose"
    class="code-preview-modal"
  >
    <div class="code-preview-container">
      <div class="file-info">
        <el-tag type="info" size="small">{{ language }}</el-tag>
        <span class="file-path">{{ filePath }}</span>
      </div>
      
      <div class="code-content" v-loading="loading">
        <pre v-if="!loading && codeContent" class="code-block"><code v-html="highlightedCode"></code></pre>
        <div v-else-if="!loading && !codeContent" class="empty-state">
          <el-empty description="No code content" :image-size="60" />
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">Close</el-button>
        <el-button type="primary" @click="handleCopy" :disabled="!codeContent">
          <el-icon><CopyDocument /></el-icon>
          Copy Code
        </el-button>
        <el-button type="success" @click="handleDownload" :disabled="!codeContent">
          <el-icon><Download /></el-icon>
          Download
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { CopyDocument, Download } from '@element-plus/icons-vue'
import hljs from 'highlight.js/lib/core'
import python from 'highlight.js/lib/languages/python'
import java from 'highlight.js/lib/languages/java'
import javascript from 'highlight.js/lib/languages/javascript'
import typescript from 'highlight.js/lib/languages/typescript'
import vue from 'highlight.js/lib/languages/xml' // Vue uses XML highlighting
import html from 'highlight.js/lib/languages/xml'
import css from 'highlight.js/lib/languages/css'
import scss from 'highlight.js/lib/languages/scss'
import json from 'highlight.js/lib/languages/json'
import xml from 'highlight.js/lib/languages/xml'
import yaml from 'highlight.js/lib/languages/yaml'

// 注册语言
hljs.registerLanguage('python', python)
hljs.registerLanguage('java', java)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('typescript', typescript)
hljs.registerLanguage('vue', vue)
hljs.registerLanguage('html', html)
hljs.registerLanguage('css', css)
hljs.registerLanguage('scss', scss)
hljs.registerLanguage('json', json)
hljs.registerLanguage('xml', xml)
hljs.registerLanguage('yaml', yaml)

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Code Preview'
  },
  filePath: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'text'
  },
  codeContent: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'close'])

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const highlightedCode = computed(() => {
  if (!props.codeContent || !props.language) return ''
  
  try {
    const result = hljs.highlight(props.codeContent, { language: props.language })
    return result.value
  } catch (error) {
    console.warn('Highlighting failed:', error)
    // 如果高亮失败，返回原始内容
    return props.codeContent.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  }
})

const handleClose = () => {
  visible.value = false
  emit('close')
}

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.codeContent)
    ElMessage.success('Code copied to clipboard')
  } catch (error) {
    console.error('Copy failed:', error)
    ElMessage.error('Failed to copy code')
  }
}

const handleDownload = () => {
  try {
    const blob = new Blob([props.codeContent], { type: 'text/plain;charset=utf-8' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = props.filePath.split('/').pop() || 'code.txt'
    link.click()
    URL.revokeObjectURL(link.href)
    ElMessage.success('File downloaded')
  } catch (error) {
    console.error('Download failed:', error)
    ElMessage.error('Failed to download file')
  }
}
</script>

<style lang="scss" scoped>
.code-preview-modal {
  :deep(.el-dialog__body) {
    padding: 0;
  }
}

.code-preview-container {
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.file-info {
  padding: 12px 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 12px;
  
  .file-path {
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.9rem;
    color: #606266;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.code-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.code-block {
  height: 100%;
  margin: 0;
  padding: 20px;
  background-color: #fafafa;
  overflow: auto;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  
  code {
    background: none;
    padding: 0;
    font-size: inherit;
    line-height: inherit;
  }
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 代码高亮样式
:deep(.hljs) {
  background: #fafafa !important;
  color: #333;
}

:deep(.hljs-comment),
:deep(.hljs-quote) {
  color: #998;
  font-style: italic;
}

:deep(.hljs-keyword),
:deep(.hljs-selector-tag),
:deep(.hljs-subst) {
  color: #333;
  font-weight: bold;
}

:deep(.hljs-number),
:deep(.hljs-literal),
:deep(.hljs-variable),
:deep(.hljs-template-variable),
:deep(.hljs-tag .hljs-attr) {
  color: #008080;
}

:deep(.hljs-string),
:deep(.hljs-doctag) {
  color: #d14;
}

:deep(.hljs-title),
:deep(.hljs-section),
:deep(.hljs-selector-id) {
  color: #900;
  font-weight: bold;
}

:deep(.hljs-subst) {
  font-weight: normal;
}

:deep(.hljs-type),
:deep(.hljs-class .hljs-title) {
  color: #458;
  font-weight: bold;
}

:deep(.hljs-tag),
:deep(.hljs-name),
:deep(.hljs-attribute) {
  color: #000080;
  font-weight: normal;
}

:deep(.hljs-regexp),
:deep(.hljs-link) {
  color: #009926;
}

:deep(.hljs-symbol),
:deep(.hljs-bullet) {
  color: #990073;
}

:deep(.hljs-built_in),
:deep(.hljs-builtin-name) {
  color: #0086b3;
}

:deep(.hljs-meta) {
  color: #999;
  font-weight: bold;
}

:deep(.hljs-deletion) {
  background: #fdd;
}

:deep(.hljs-addition) {
  background: #dfd;
}

:deep(.hljs-emphasis) {
  font-style: italic;
}

:deep(.hljs-strong) {
  font-weight: bold;
}
</style>
