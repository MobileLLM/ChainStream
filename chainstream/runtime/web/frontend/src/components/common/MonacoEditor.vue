<template>
  <div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as monaco from 'monaco-editor'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'python'
  },
  theme: {
    type: String,
    default: 'vs-dark'
  },
  height: {
    type: String,
    default: '400px'
  },
  readOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const editorContainer = ref(null)
let editor = null

const initEditor = async () => {
  if (!editorContainer.value) return

  editor = monaco.editor.create(editorContainer.value, {
    value: props.modelValue,
    language: props.language,
    theme: props.theme,
    readOnly: props.readOnly,
    automaticLayout: true,
    minimap: { enabled: false },
    scrollBeyondLastLine: false,
    fontSize: 14,
    lineNumbers: 'on',
    roundedSelection: false,
    scrollbar: {
      vertical: 'auto',
      horizontal: 'auto'
    },
    wordWrap: 'on',
    folding: true,
    lineDecorationsWidth: 10,
    lineNumbersMinChars: 3
  })

  // 监听内容变化
  editor.onDidChangeModelContent(() => {
    const value = editor.getValue()
    emit('update:modelValue', value)
    emit('change', value)
  })
}

const updateValue = (newValue) => {
  if (editor && editor.getValue() !== newValue) {
    editor.setValue(newValue)
  }
}

// 监听props变化
watch(() => props.modelValue, (newValue) => {
  updateValue(newValue)
})

watch(() => props.language, (newLanguage) => {
  if (editor) {
    monaco.editor.setModelLanguage(editor.getModel(), newLanguage)
  }
})

watch(() => props.theme, (newTheme) => {
  if (editor) {
    monaco.editor.setTheme(newTheme)
  }
})

onMounted(async () => {
  await nextTick()
  initEditor()
})

onUnmounted(() => {
  if (editor) {
    editor.dispose()
  }
})

defineExpose({
  editor: () => editor,
  getValue: () => editor ? editor.getValue() : '',
  setValue: (value) => updateValue(value),
  focus: () => editor ? editor.focus() : null
})
</script>

<style scoped>
.monaco-editor-container {
  width: 100%;
  height: v-bind(height);
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
