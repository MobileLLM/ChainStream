<template>
  <div class="generator-container">
    <div class="generator-header" ref="headerRef">
      <h2>{{ $t('generator.codeGenerator') }}</h2>
      <div class="header-actions">
        <!-- <el-input v-model="currentFilePath" size="small" placeholder="文件路径（相对 AgentStore）" style="width: 320px" /> -->
        <el-button size="small" @click="openNewDialog">
          <el-icon><FolderOpened /></el-icon>
          {{ $t('generator.new') }}
        </el-button>
        <el-button size="small" @click="openLoadDialog">
          <el-icon><Refresh /></el-icon>
          {{ $t('generator.load') }}
        </el-button>
        <el-button size="small" type="primary" @click="saveFile">
          <el-icon><UploadFilled /></el-icon>
          {{ $t('generator.save') }}
        </el-button>
        <el-button size="small" @click="openSaveAsDialog">{{ $t('generator.saveAs') }}</el-button>
        <!-- <el-button size="small" type="primary" @click="generateCode" :loading="isGenerating">
          <el-icon><Star /></el-icon>
          生成代码
        </el-button> -->
      </div>
    </div>

    <el-container class="generator-content" ref="contentRef" :style="gridStyle">
      <!-- 左侧：代码编辑区 -->
      <div class="editor-panel">
        <div class="panel-header">
          <h3>{{ $t('generator.codeEditor') }}</h3>
          <div class="editor-actions">
            <el-tag :type="selectedLanguage === 'python' ? 'success' : 'primary'" size="large">
              {{ selectedLanguage === 'python' ? 'Python' : 'Java' }}
            </el-tag>
            <el-button size="small" @click="clearCode">
              <el-icon><Delete /></el-icon>
              {{ $t('generator.clear') }}
            </el-button>
            <el-button size="small" @click="copyCode">
              <el-icon><Document /></el-icon>
              {{ $t('generator.copy') }}
            </el-button>
          </div>
        </div>
        <div class="editor-container">
          <MonacoEditor
            v-model="generatedCode"
            :language="monacoLanguage"
            height="100%"
            @change="onCodeChange"
          />
        </div>
      </div>

      <!-- 中间拖拽条 -->
      <div class="splitter" @mousedown="startResize"></div>

      <!-- 右侧：对话区 -->
      <div class="chat-panel">
        <div class="panel-header">
          <h3>{{ $t('generator.aiChat') }}</h3>
          <div class="chat-actions">
            <el-select v-model="selectedGenerator" size="small" style="width: 220px" :placeholder="$t('generator.selectGenerator')">
              <el-option :label="$t('generator.pythonSingle')" value="python_single" />
              <el-option :label="$t('generator.javaSingle')" value="java_single" />
              <el-option :label="$t('generator.sandboxIter')" value="sandbox_iter" disabled />
              <el-option :label="$t('generator.exceptionHandler')" value="exception_handler" disabled />
            </el-select>
            <el-button size="small" @click="showMemoryDialog">
              <el-icon><View /></el-icon>
              {{ $t('generator.viewMemory') }}
            </el-button>
            <el-button size="small" type="warning" @click="performSecurityCheck" :disabled="isCheckingSecurity">
              <el-icon v-if="!isCheckingSecurity"><Lock /></el-icon>
              <el-icon v-else class="is-loading"><Loading /></el-icon>
              {{ isCheckingSecurity ? $t('generator.checking') : $t('generator.securityCheck') }}
            </el-button>
            <el-button size="small" @click="clearChat">
              <el-icon><Delete /></el-icon>
              {{ $t('generator.clearChat') }}
            </el-button>
          </div>
        </div>
        <el-container class="chat-col">
          <el-main class="chat-main-scroll">
            <div class="chat-messages" ref="chatMessagesRef">
              <div
                v-for="(message, index) in chatMessages"
                :key="index"
                :class="['message', message.role]"
              >
                <div class="message-content" :class="message.role === 'user' ? 'bubble-user' : 'bubble-assistant'">
                  <div v-if="!message.loading" class="message-main" v-html="formatMessage(message.content)"></div>
                  <div v-else class="message-loading">
                    <el-icon class="is-loading"><Loading /></el-icon>
                    {{ $t('generator.generating') }}
                  </div>
                  <div v-if="message.stats" class="message-stats">{{ formatStats(message.stats) }}</div>
                </div>
              </div>
            </div>
          </el-main>
          <el-footer class="chat-footer" height="110px">
            <div class="chat-input">
              <div class="input-row">
    <el-input
                  v-model="userInput"
      type="textarea"
                  :rows="3"
                  :placeholder="$t('generator.inputPlaceholder')"
                  @keydown.ctrl.enter="sendMessage"
                />
                <el-button type="primary" @click="sendMessage" :loading="isGenerating" class="send-btn">
                  <el-icon><Coffee /></el-icon>
                  {{ $t('generator.send') }}
                </el-button>
              </div>
            </div>
          </el-footer>
        </el-container>
    </div>
    </el-container>

    <!-- 路径浏览器对话框 -->
    <el-dialog v-model="showFileDialog" :title="getBrowserTitle()" width="70%" :before-close="handleFileDialogClose">
      <div class="path-browser">
        <div class="breadcrumbs">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item @click="loadDirectory('')" style="cursor:pointer">{{ $t('generator.agentStore') }}</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(seg, idx) in breadcrumbs" :key="idx">
              <span style="cursor:pointer" @click="onBreadcrumbClick(idx)">{{ seg }}</span>
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <el-table :data="browserItems" v-loading="browserLoading" height="360px" @row-click="onRowClick" highlight-current-row>
          <el-table-column :label="$t('generator.name')" min-width="320">
            <template #default="{ row }">
              <el-icon v-if="row.isDirectory" style="margin-right:6px"><Folder /></el-icon>
              <el-icon v-else style="margin-right:6px"><Document /></el-icon>
              <span>{{ row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column :label="$t('generator.type')" width="120">
            <template #default="{ row }">{{ row.isDirectory ? $t('generator.directory') : $t('generator.file') }}</template>
          </el-table-column>
          <el-table-column :label="$t('generator.size')" width="120">
            <template #default="{ row }">{{ row.size || '-' }}</template>
          </el-table-column>
        </el-table>
        <div v-if="browserMode === 'new' || browserMode === 'saveAs'" class="save-as-bar">
          <el-input v-model="browserFilename" :placeholder="`${$t('generator.enterFilename')} hello${getFileExtension(selectedLanguage)}`" />
        </div>
      </div>
      <template #footer>
        <el-button @click="showFileDialog = false">{{ $t('common.cancel') }}</el-button>
        <el-button type="primary" @click="confirmFileSelection">{{ getBrowserButtonText() }}</el-button>
      </template>
    </el-dialog>

    <!-- 查看记忆对话框 -->
    <el-dialog v-model="showMemoryDialogVisible" :title="$t('generator.sessionMemory')" width="60%">
      <div class="memory-content">
        <el-alert v-if="!sessionMemory" type="info" :closable="false" show-icon>
          {{ $t('generator.noMemoryYet') }}
        </el-alert>
        <el-input
          v-else
          v-model="sessionMemory"
          type="textarea"
          :rows="15"
          readonly
          :placeholder="$t('generator.sessionMemory')"
        />
      </div>
      <template #footer>
        <el-button @click="showMemoryDialogVisible = false">{{ $t('common.close') }}</el-button>
        <el-button v-if="sessionMemory" type="danger" @click="clearMemory">{{ $t('generator.clearMemory') }}</el-button>
      </template>
    </el-dialog>

    <!-- 安全检查结果对话框 -->
    <el-dialog v-model="showSecurityDialog" :title="$t('generator.securityReport')" width="70%" :before-close="handleSecurityDialogClose">
      <div class="security-report">
        <!-- 总体结果 -->
        <el-alert 
          :type="securityResult?.overall_safe ? 'success' : 'error'" 
          :title="securityResult?.overall_safe ? $t('generator.securityPassed') : $t('generator.securityIssues')" 
          :closable="false"
          show-icon
          class="security-summary">
          <template #default>
            <div class="summary-text">{{ securityResult?.summary || $t('generator.checking') }}</div>
            <div v-if="securityElapsedMs" class="summary-time">{{ $t('generator.checkTime') }}: {{ securityElapsedMs }}ms</div>
          </template>
        </el-alert>

        <!-- 代码检查 -->
        <el-card class="security-section" shadow="never">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon v-if="securityResult?.code_check?.safe" style="color: #67c23a"><CircleCheck /></el-icon>
                <el-icon v-else style="color: #f56c6c"><CircleClose /></el-icon>
                {{ $t('generator.codeContent') }}
              </span>
              <el-tag :type="securityResult?.code_check?.safe ? 'success' : 'danger'" size="small">
                {{ securityResult?.code_check?.safe ? $t('generator.safe') : $t('generator.hasIssues') }}
              </el-tag>
            </div>
          </template>
          <div class="section-content">
            <p class="details-text">{{ securityResult?.code_check?.details || $t('generator.noDetails') }}</p>
            <el-alert 
              v-if="securityResult?.code_check?.issues && securityResult.code_check.issues.length > 0"
              type="error"
              :closable="false"
              class="issues-alert">
              <ul class="issues-list">
                <li v-for="(issue, idx) in securityResult.code_check.issues" :key="idx">{{ issue }}</li>
              </ul>
            </el-alert>
          </div>
        </el-card>

        <!-- 消息检查 -->
        <el-card class="security-section" shadow="never">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon v-if="securityResult?.messages_check?.safe" style="color: #67c23a"><CircleCheck /></el-icon>
                <el-icon v-else style="color: #f56c6c"><CircleClose /></el-icon>
                {{ $t('generator.chatMessages') }}
              </span>
              <el-tag :type="securityResult?.messages_check?.safe ? 'success' : 'danger'" size="small">
                {{ securityResult?.messages_check?.safe ? $t('generator.safe') : $t('generator.hasIssues') }}
              </el-tag>
            </div>
          </template>
          <div class="section-content">
            <p class="details-text">{{ securityResult?.messages_check?.details || $t('generator.noDetails') }}</p>
            <el-alert 
              v-if="securityResult?.messages_check?.issues && securityResult.messages_check.issues.length > 0"
              type="error"
              :closable="false"
              class="issues-alert">
              <ul class="issues-list">
                <li v-for="(issue, idx) in securityResult.messages_check.issues" :key="idx">{{ issue }}</li>
              </ul>
            </el-alert>
          </div>
        </el-card>

        <!-- 记忆检查 -->
        <el-card class="security-section" shadow="never">
          <template #header>
            <div class="section-header">
              <span class="section-title">
                <el-icon v-if="securityResult?.memory_check?.safe" style="color: #67c23a"><CircleCheck /></el-icon>
                <el-icon v-else style="color: #f56c6c"><CircleClose /></el-icon>
                {{ $t('generator.sessionMemory') }}
              </span>
              <el-tag :type="securityResult?.memory_check?.safe ? 'success' : 'danger'" size="small">
                {{ securityResult?.memory_check?.safe ? $t('generator.safe') : $t('generator.hasIssues') }}
              </el-tag>
            </div>
          </template>
          <div class="section-content">
            <p class="details-text">{{ securityResult?.memory_check?.details || $t('generator.noDetails') }}</p>
            <el-alert 
              v-if="securityResult?.memory_check?.issues && securityResult.memory_check.issues.length > 0"
              type="error"
              :closable="false"
              class="issues-alert">
              <ul class="issues-list">
                <li v-for="(issue, idx) in securityResult.memory_check.issues" :key="idx">{{ issue }}</li>
              </ul>
            </el-alert>
          </div>
        </el-card>
      </div>
      <template #footer>
        <el-button @click="showSecurityDialog = false">{{ $t('common.close') }}</el-button>
        <el-button v-if="!securityResult?.overall_safe" type="danger" @click="handleSecurityIssues">{{ $t('generator.handleIssues') }}</el-button>
      </template>
    </el-dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch, onBeforeUnmount } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Star,
  Delete,
  Document,
  UploadFilled,
  Coffee,
  FolderOpened,
  Refresh,
  Folder,
  Loading,
  View,
  Lock,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'
import Prism from 'prismjs'
import 'prismjs/themes/prism-tomorrow.css'
// 依赖顺序很重要：不少语言依赖 clike
import 'prismjs/components/prism-clike'
// C++ 依赖 C 语法
import 'prismjs/components/prism-c'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-java'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-cpp'
import 'prismjs/components/prism-go'
import MonacoEditor from '@/components/common/MonacoEditor.vue'
import request from '@/utils/request.js'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 响应式数据
const generatedCode = ref('')
const userInput = ref('')
const chatMessages = ref([])
const isGenerating = ref(false)
const sessionMemory = ref('')
const selectedGenerator = ref('python_single')
const contentRef = ref(null)
const headerRef = ref(null)
const editorWidthPercent = ref(66)
let isResizing = false
const contentHeight = ref(0)
const selectedLanguage = ref('python')
const showFileDialog = ref(false)
const showMemoryDialogVisible = ref(false)
const fileTreeData = ref([])
const selectedFile = ref(null)
const expandedKeys = ref([])
const chatMessagesRef = ref(null)
const codeEditorRef = ref(null)
const currentFilePath = ref('')
const showSecurityDialog = ref(false)
const isCheckingSecurity = ref(false)
const securityResult = ref(null)
const securityElapsedMs = ref(null)
const monacoLanguage = computed(() => {
  const map = { python: 'python', java: 'java', javascript: 'javascript', typescript: 'typescript', cpp: 'cpp', go: 'go' }
  return map[selectedLanguage.value] || 'plaintext'
})

// 使用CSS Grid控制左右宽度，保持总宽度不超过容器
const gridStyle = computed(() => ({
  display: 'grid',
  gridTemplateColumns: `${editorWidthPercent.value}% 6px ${100 - editorWidthPercent.value}%`,
  columnGap: '0',
  width: '100%',
  overflow: 'hidden'
}))

// 路径浏览器状态
const browserMode = ref('load') // 'load' | 'saveAs'
const browserLoading = ref(false)
const browserCurrentPath = ref('')
const browserItems = ref([])
const browserSelectedItem = ref(null)
const browserFilename = ref('')
const breadcrumbs = ref([])

// 树形组件配置
const treeProps = {
  children: 'children',
  label: 'name'
}

// 计算属性 - 代码高亮
const highlightedCode = computed(() => {
  if (!generatedCode.value) return ''
  
  try {
    const highlighted = Prism.highlight(
      generatedCode.value,
      Prism.languages[selectedLanguage.value] || Prism.languages.python,
      selectedLanguage.value
    )
    return highlighted
  } catch (error) {
    console.error('Code highlighting error:', error)
    return generatedCode.value
  }
})

// 检测代码语言
const detectLanguage = (code, filename = '') => {
  // 首先根据文件名扩展名判断
  if (filename) {
    const ext = filename.toLowerCase().split('.').pop()
    if (ext === 'py') return 'python'
    if (ext === 'java') return 'java'
  }
  
  // 根据内容特征判断（只支持Python和Java）
  if (code.includes('def ') || code.includes('import ') || code.includes('from ') || code.includes('print(')) {
    return 'python'
  } else if (code.includes('public class') || code.includes('import java') || code.includes('System.out.println')) {
    return 'java'
  }
  
  // 默认返回python
  return 'python'
}

// 代码变化处理
const onCodeChange = (value) => {
  generatedCode.value = value
  selectedLanguage.value = detectLanguage(value)
}

// 生成代码
const generateCode = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入您的需求')
    return
  }

  isGenerating.value = true
  
  try {
    // 添加用户消息
    chatMessages.value.push({
      role: 'user',
      content: userInput.value
    })

    // 模拟AI生成代码
    const response = await simulateCodeGeneration(userInput.value)
    
    // 添加AI回复
    chatMessages.value.push({
      role: 'assistant',
      content: response
    })

    // 提取代码并设置到编辑器
    const codeMatch = response.match(/```(\w+)?\n([\s\S]*?)```/)
    if (codeMatch) {
      const language = codeMatch[1] || 'python'
      const code = codeMatch[2]
      generatedCode.value = code
      selectedLanguage.value = language
    }

    userInput.value = ''
    scrollToBottom()
    
  } catch (error) {
    ElMessage.error('生成代码失败: ' + error.message)
  } finally {
    isGenerating.value = false
  }
}

// 模拟代码生成
const simulateCodeGeneration = async (prompt) => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // 根据提示生成不同的代码示例
  if (prompt.includes('Python') || prompt.includes('python')) {
    return `根据您的需求，我生成了以下Python代码：

\`\`\`python
def hello_world():
    """简单的Hello World函数"""
    print("Hello, World!")
    return "Hello, World!"

class Calculator:
    """简单的计算器类"""
    
    def __init__(self):
        self.result = 0
    
    def add(self, x, y):
        """加法运算"""
        self.result = x + y
        return self.result
    
    def multiply(self, x, y):
        """乘法运算"""
        self.result = x * y
        return self.result

if __name__ == "__main__":
    # 使用示例
    calc = Calculator()
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"4 * 5 = {calc.multiply(4, 5)}")
    
    hello_world()
\`\`\`

这个代码包含了一个简单的函数和一个计算器类，展示了Python的基本语法和面向对象编程。`
  } else if (prompt.includes('Java') || prompt.includes('java')) {
    return `根据您的需求，我生成了以下Java代码：

\`\`\`java
public class HelloWorld {
    private String message;
    
    public HelloWorld(String message) {
        this.message = message;
    }
    
    public void printMessage() {
        System.out.println(message);
    }
    
    public static void main(String[] args) {
        HelloWorld hello = new HelloWorld("Hello, World!");
        hello.printMessage();
        
        // 简单的计算示例
        Calculator calc = new Calculator();
        System.out.println("2 + 3 = " + calc.add(2, 3));
    }
}

class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int multiply(int a, int b) {
        return a * b;
    }
}
\`\`\`

这个Java代码展示了类的基本结构、构造函数、方法和main方法的使用。`
  } else {
    return `根据您的需求，我生成了以下代码：

\`\`\`python
# 这是一个通用的代码模板
def main():
    """主函数"""
    print("欢迎使用代码生成器！")
    
    # 在这里添加您的业务逻辑
    process_data()
    
def process_data():
    """处理数据的函数"""
    data = [1, 2, 3, 4, 5]
    result = sum(data)
    print(f"数据总和: {result}")
    
    return result

if __name__ == "__main__":
    main()
\`\`\`

这是一个通用的Python代码模板，您可以根据具体需求进行修改。`
  }
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim()) return
  
  // 添加用户消息
  chatMessages.value.push({ role: 'user', content: userInput.value })
  
  const message = userInput.value
  userInput.value = ''
  
  // 滚动到底部
  scrollToBottom()
  
  // 添加占位loading消息
  chatMessages.value.push({ role: 'assistant', content: '', loading: true })
  const loadingIndex = chatMessages.value.length - 1
  scrollToBottom()

  // 调用后端生成接口
  try {
    const data = await request.post('/generator/chat', {
      message,
      code: generatedCode.value || '',
      language: selectedLanguage.value,
      path: currentFilePath.value,
      memory: sessionMemory.value,
      generator_type: selectedGenerator.value
    })
    // 期望返回：{ success, reply, new_code, stats }
    const reply = data?.reply || '（无内容）'
    const newCode = data?.new_code
    const stats = data?.stats
    const newMemory = data?.new_memory
    // 替换loading消息（使用数组赋值确保视图更新）
    const prev = chatMessages.value[loadingIndex] || { role: 'assistant' }
    chatMessages.value[loadingIndex] = { ...prev, loading: false, content: reply, stats }
    if (typeof newCode === 'string') {
      generatedCode.value = newCode
    }
    if (typeof newMemory === 'string') {
      sessionMemory.value = newMemory
    }
  } catch (err) {
    const prev = chatMessages.value[loadingIndex] || { role: 'assistant' }
    chatMessages.value[loadingIndex] = { ...prev, loading: false, content: `服务暂时不可用：${err?.message || 'unknown'}` }
  }
  scrollToBottom()
}

// 格式化消息
const formatMessage = (content) => {
  // 简单的markdown格式化
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/\n/g, '<br>')
}

// 统计信息格式化（小字展示）
const formatStats = (s) => {
  if (!s) return ''
  const pt = s.prompt_tokens ?? '-'
  const ct = s.completion_tokens ?? '-'
  const tt = s.total_tokens ?? '-'
  const ms = s.elapsed_ms ?? '-'
  return `tokens: ${tt} (p:${pt}/c:${ct}) · ${ms}ms`
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
}

// 根据全局header+本页header动态计算可用高度
const updateContentHeight = () => {
  nextTick(() => {
    const contentEl = contentRef.value
    if (!contentEl) return
    const rect = contentEl.getBoundingClientRect()
    const viewportH = window.innerHeight
    const h = viewportH - rect.top
    contentHeight.value = h > 400 ? h : 400
  })
}

// 拖拽调整左右宽度
const startResize = (e) => {
  isResizing = true
  document.body.style.cursor = 'col-resize'
  const startX = e.clientX
  const containerRect = contentRef.value?.getBoundingClientRect()
  const startPercent = editorWidthPercent.value
  
  const onMove = (ev) => {
    if (!isResizing) return
    const rect = contentRef.value?.getBoundingClientRect()
    if (!rect) return
    const delta = ev.clientX - startX
    const newPx = (startPercent / 100) * rect.width + delta
    let percent = Math.round((newPx / rect.width) * 100)
    percent = Math.min(85, Math.max(15, percent))
    editorWidthPercent.value = percent
  }
  const onUp = () => {
    isResizing = false
    document.body.style.cursor = ''
    window.removeEventListener('mousemove', onMove)
    window.removeEventListener('mouseup', onUp)
  }
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', onUp)
}

// 清空代码
const clearCode = () => {
  ElMessageBox.confirm(t('generator.confirmClearCode'), t('common.confirm'), {
    confirmButtonText: t('common.confirm'),
    cancelButtonText: t('common.cancel'),
    type: 'warning'
  }).then(() => {
    generatedCode.value = ''
    ElMessage.success(t('generator.codeCleared'))
  })
}

// 复制代码
const copyCode = async () => {
  if (!generatedCode.value) {
    ElMessage.warning(t('generator.noCodeToCopy'))
    return
  }
  
  try {
    await navigator.clipboard.writeText(generatedCode.value)
    ElMessage.success(t('generator.codeCopied'))
  } catch (error) {
    ElMessage.error(t('generator.copyFailed'))
  }
}

// 保存代码（编辑器内的保存按钮，与顶部保存按钮功能相同）
const saveCode = () => {
  saveFile()
}

// 获取文件扩展名（只支持Python和Java）
const getFileExtension = (language) => {
  return language === 'java' ? '.java' : '.py'
}

// 显示记忆对话框
const showMemoryDialog = () => {
  showMemoryDialogVisible.value = true
}

// 清空记忆
const clearMemory = () => {
  ElMessageBox.confirm(t('generator.confirmClearMemory'), t('common.confirm'), {
    confirmButtonText: t('common.confirm'),
    cancelButtonText: t('common.cancel'),
    type: 'warning'
  }).then(() => {
    sessionMemory.value = ''
    showMemoryDialogVisible.value = false
    ElMessage.success(t('generator.memoryCleared'))
  }).catch(() => {})
}

// 清空对话
const clearChat = () => {
  ElMessageBox.confirm(t('generator.confirmClearChat'), t('common.confirm'), {
    confirmButtonText: t('common.confirm'),
    cancelButtonText: t('common.cancel'),
    type: 'warning'
  }).then(() => {
    chatMessages.value = []
    ElMessage.success(t('generator.chatCleared'))
  })
}

// 执行安全检查
const performSecurityCheck = async () => {
  if (!generatedCode.value && chatMessages.value.length === 0 && !sessionMemory.value) {
    ElMessage.warning(t('generator.noContentToCheck'))
    return
  }

  isCheckingSecurity.value = true
  securityResult.value = null
  securityElapsedMs.value = null

  try {
    const data = await request.post('/generator/security-check', {
      code: generatedCode.value || '',
      messages: chatMessages.value,
      memory: sessionMemory.value || ''
    })

    if (data?.success) {
      securityResult.value = data.result
      securityElapsedMs.value = data.elapsed_ms
      showSecurityDialog.value = true

      // 如果有安全问题，显示警告通知
      if (!data.result?.overall_safe) {
        ElMessage.warning(t('generator.securityWarning'))
      } else {
        ElMessage.success(t('generator.securityPassed'))
      }
    } else {
      ElMessage.error(t('generator.securityCheckFailed') + ': ' + (data?.error || 'unknown'))
    }
  } catch (err) {
    ElMessage.error(t('generator.securityCheckFailed') + ': ' + (err?.message || 'unknown'))
  } finally {
    isCheckingSecurity.value = false
  }
}

// 处理安全对话框关闭
const handleSecurityDialogClose = () => {
  showSecurityDialog.value = false
}

// 处理安全问题
const handleSecurityIssues = () => {
  ElMessageBox.alert(
    t('generator.securityAdvice'),
    t('generator.securityAdviceTitle'),
    {
      confirmButtonText: t('generator.iKnow'),
      type: 'warning'
    }
  )
}

// 加载AgentStore
const loadFromAgentStore = async () => {
  browserMode.value = 'load'
  showFileDialog.value = true
  await loadDirectory('')
}

const loadDirectory = async (path = '') => {
  try {
    browserLoading.value = true
    const data = await request.get('/monitor/agents/directory', { params: { path } })
    // data: { items, currentPath, pathSegments, agentStorePath }
    browserItems.value = (data.items || []).map(it => ({
      name: it.name,
      isDirectory: !!(it.isDirectory ?? it.is_dir),
      size: it.size,
      path: it.path || it.relativePath || it.relative_path || it.name
    }))
    browserCurrentPath.value = (data.currentPath || '').replace(/\\/g, '/')
    breadcrumbs.value = Array.isArray(data.pathSegments) ? data.pathSegments : (browserCurrentPath.value ? browserCurrentPath.value.split('/').filter(Boolean) : [])
    browserSelectedItem.value = null
  } catch (error) {
    ElMessage.error(t('generator.readDirFailed') + ': ' + (error?.message || 'unknown'))
  } finally {
    browserLoading.value = false
  }
}

// 获取展开的键
const getExpandedKeys = (items) => {
  const keys = []
  const traverse = (nodes) => {
    nodes.forEach(node => {
      if (node.isDirectory && node.children && node.children.length > 0) {
        keys.push(node.path)
        traverse(node.children)
      }
    })
  }
  traverse(items)
  return keys
}

// 构建文件树
const buildFileTree = (items) => {
  const tree = []
  const pathMap = {}
  
  items.forEach(item => {
    const pathParts = item.name.split('/')
    let currentPath = ''
    let parent = null
    
    pathParts.forEach((part, index) => {
      currentPath = currentPath ? `${currentPath}/${part}` : part
      
      if (!pathMap[currentPath]) {
        const node = {
          name: part,
          path: currentPath,
          isDirectory: index < pathParts.length - 1 || item.isDirectory,
          children: []
        }
        
        if (parent) {
          parent.children.push(node)
        } else {
          tree.push(node)
        }
        
        pathMap[currentPath] = node
      }
      
      parent = pathMap[currentPath]
    })
  })
  
  return tree
}

// 处理节点点击
const handleNodeClick = (data) => {
  selectedFile.value = data
}

// 确认文件选择
const confirmFileSelection = async () => {
  if (browserMode.value === 'load') {
    // 载入模式：必须选择一个文件
    if (!browserSelectedItem.value || browserSelectedItem.value.isDirectory) {
      ElMessage.warning(t('generator.selectFile'))
      return
    }
    try {
      const data = await request.get('/generator/load', { params: { path: browserSelectedItem.value.path } })
      if (!data?.success) {
        ElMessage.error(t('generator.loadFileFailed') + ': ' + (data?.error || 'unknown'))
        return
      }
      generatedCode.value = data.content || ''
      selectedLanguage.value = detectLanguage(data.content || '', data.path || browserSelectedItem.value.path || '')
      currentFilePath.value = data.path || browserSelectedItem.value.path || ''
      showFileDialog.value = false
      ElMessage.success(t('generator.loadFileSuccess'))
    } catch (e) {
      ElMessage.error(t('generator.loadFileFailed') + ': ' + (e?.message || 'unknown'))
    }
  } else {
    // 新建/另存为模式：需要输入文件名
    if (!browserFilename.value.trim()) {
      ElMessage.warning(t('generator.enterFilenamePrompt'))
      return
    }
    
    // 确定保存目录：如果选中目录则用选中的，否则用当前目录
    let saveDir = browserCurrentPath.value
    if (browserSelectedItem.value && browserSelectedItem.value.isDirectory) {
      saveDir = browserSelectedItem.value.path
    }
    
    // 构建完整路径
    const fullPath = saveDir ? `${saveDir}/${browserFilename.value}` : browserFilename.value
    
    try {
      await doSaveToPath(fullPath, false) // 新建/另存为，不允许覆盖
      showFileDialog.value = false
    } catch (e) {
      ElMessage.error(t('generator.saveFailed') + ': ' + (e?.message || 'unknown'))
    }
  }
}

// 处理对话框关闭
const handleFileDialogClose = () => {
  selectedFile.value = null
  showFileDialog.value = false
}

// 监听语言变化
watch(selectedLanguage, () => {
  // 语言变化时重新高亮代码
  nextTick(() => {
    if (codeEditorRef.value) {
      // 触发重新渲染
    }
  })
})

// 组件挂载
onMounted(() => {
  // 初始化代码编辑器
  if (codeEditorRef.value) {
    // 可以在这里添加更多初始化逻辑
  }
  if (chatMessages.value.length === 0) {
    const welcomeMessage = t('generator.aiChat') === 'AI Chat' 
      ? 'Hello, I am the generation assistant. Please describe your requirements, and I will provide suggestions and generate code based on the current code.'
      : '你好，我是生成助手。请描述你的需求，我会基于当前代码进行建议与生成。'
    chatMessages.value.push({ role: 'assistant', content: welcomeMessage })
  }
  updateContentHeight()
  window.addEventListener('resize', updateContentHeight)
  window.addEventListener('beforeunload', beforeUnloadHandler)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateContentHeight)
  window.removeEventListener('beforeunload', beforeUnloadHandler)
})

// 顶部按钮动作
const openLoadDialog = () => {
  browserMode.value = 'load'
  showFileDialog.value = true
  loadDirectory('')
}

const openNewDialog = async () => {
  // 如果有当前代码且有文件路径，先自动保存
  if (generatedCode.value && currentFilePath.value) {
    try {
      await doSaveToPath(currentFilePath.value, true) // 自动保存，允许覆盖
      ElMessage.success(t('generator.autoSaved'))
    } catch (e) {
      ElMessage.warning(t('generator.autoSaveFailed'))
      return
    }
  }
  
  // 弹出语言选择对话框
  try {
    const { value: language } = await ElMessageBox.confirm(
      t('generator.selectLanguage'),
      t('generator.newFile'),
      {
        distinguishCancelAndClose: true,
        confirmButtonText: 'Python',
        cancelButtonText: 'Java',
        type: 'success',
        confirmButtonClass: 'el-button--success',
        cancelButtonClass: 'el-button--primary'
      }
    )
    
    // 确认选择Python
    selectedLanguage.value = 'python'
    browserFilename.value = ''
  } catch (action) {
    if (action === 'cancel') {
      // 选择Java
      selectedLanguage.value = 'java'
      browserFilename.value = ''
    } else {
      // 用户关闭了对话框
      return
    }
  }
  
  // 清空内容，打开文件浏览器
  generatedCode.value = ''
  currentFilePath.value = ''
  browserMode.value = 'new'
  showFileDialog.value = true
  await loadDirectory('')
}

const openSaveAsDialog = async () => {
  // 另存为：选择目录+输入文件名
  browserMode.value = 'saveAs'
  browserFilename.value = ''
  showFileDialog.value = true
  await loadDirectory('')
}

const saveFile = async () => {
  // 保存：直接写入当前路径，如果没有当前路径则触发另存为
  if (!currentFilePath.value) {
    return openSaveAsDialog()
  }
  await doSaveToPath(currentFilePath.value, true) // 保存到当前文件，允许覆盖
}

const doSaveToPath = async (filePath, allowOverwrite = false) => {
  try {
    const extension = getFileExtension(selectedLanguage.value)
    const finalPath = filePath.endsWith(extension) ? filePath : `${filePath}${extension}`
    
    const data = await request.post('/generator/save', {
      file_path: finalPath,
      content: generatedCode.value || '', // 允许保存空文件
      language: selectedLanguage.value,
      allow_overwrite: allowOverwrite
    })
    
    if (data?.success) {
      currentFilePath.value = finalPath
      ElMessage.success(t('generator.saveSuccess'))
    } else {
      ElMessage.error(t('generator.saveFailed') + ': ' + (data?.error || 'unknown'))
    }
  } catch (e) {
    // 处理HTTP错误响应
    if (e?.response?.data?.error) {
      ElMessage.error(e.response.data.error)
    } else {
      ElMessage.error(t('generator.saveFailed') + ': ' + (e?.message || 'unknown'))
    }
  }
}

// 路径浏览器交互
const onRowClick = (row) => {
  browserSelectedItem.value = row
  if (row.isDirectory) {
    loadDirectory(row.path)
  }
}

const onBreadcrumbClick = (idx) => {
  const path = breadcrumbs.value.slice(0, idx + 1).join('/')
  loadDirectory(path)
}

const getBrowserTitle = () => {
  switch (browserMode.value) {
    case 'load': return t('generator.selectFile')
    case 'new': return t('generator.newFile')
    case 'saveAs': return t('generator.saveAs')
    default: return t('generator.browserTitle')
  }
}

const getBrowserButtonText = () => {
  switch (browserMode.value) {
    case 'load': return t('generator.select')
    case 'new': return t('generator.new')
    case 'saveAs': return t('generator.save')
    default: return t('common.confirm')
  }
}

// 关闭/刷新提醒：记忆memory仅保存在本页会话中
const beforeUnloadHandler = (e) => {
  if (sessionMemory.value && sessionMemory.value.length > 0) {
    e.preventDefault()
    // Chrome需要设置returnValue
    e.returnValue = ''
    return ''
  }
}

// 路由离开确认：有memory时提示
onBeforeRouteLeave((to, from, next) => {
  if (!sessionMemory.value || sessionMemory.value.length === 0) {
    return next()
  }
  ElMessageBox.confirm(t('generator.leaveConfirm'), t('generator.confirmLeave'), {
    type: 'warning',
    confirmButtonText: t('generator.continueLeave'),
    cancelButtonText: t('common.cancel')
  }).then(() => next()).catch(() => next(false))
})
</script>

<style scoped>
.generator-container {
  /* 不再强制100vh，避免遮蔽全局header，交给父容器控制 */
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.generator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.generator-header h2 {
  margin: 0;
  color: #303133;
  font-size: 20px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.generator-content {
  /* 使用固定高度：视口高度 - 180px，避免超出，同时基本占满 */
  height: calc(100vh - 130px);
  display: flex;
  min-height: 560px; /* 给一个合理的最小高度，避免太小 */
}

.editor-panel, .chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  margin: 8px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  min-height: 0; /* 关键：避免子容器溢出 */
}
.chat-col {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0; /* 允许子元素在垂直方向收缩，启用内部滚动 */
}

.chat-main-scroll {
  padding: 0; /* 由chat-messages控制内边距 */
  flex: 1;            /* 填充剩余空间 */
  display: flex;      /* 让内部chat-messages使用flex:1生效 */
  min-height: 0;      /* 关键：允许内部滚动 */
}

.chat-footer {
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.splitter {
  width: 6px;
  cursor: col-resize;
  background: #e4e7ed;
  border-left: 1px solid #dcdfe6;
  border-right: 1px solid #dcdfe6;
  height: 100%;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* 改为顶部对齐，避免按钮组太高时被挤 */
  padding: 16px 20px;
  background: #fafafa;
  border-bottom: 1px solid #e4e7ed;
  gap: 12px; /* 标题和按钮组之间的间距 */
  flex-wrap: wrap; /* 允许换行 */
}

.panel-header + .editor-container,
.panel-header + .chat-container {
  /* 保证header占据固定高度后，内容区剩余高度可滚动 */
  min-height: 0;
}

.panel-header h3 {
  margin: 0;
  color: #303133;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0; /* 防止标题被压缩 */
  line-height: 32px; /* 与按钮对齐 */
}

.editor-actions, .chat-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap; /* 允许按钮换行 */
}

.chat-actions {
  width: 100%; /* 确保有足够的空间 */
}

.chat-actions .el-select {
  flex-shrink: 0; /* 防止下拉框被压缩 */
  min-width: 180px;
  max-width: 220px;
}

.chat-actions .el-button {
  flex-shrink: 0; /* 防止按钮被压缩 */
  white-space: nowrap; /* 防止按钮文字换行 */
}

.editor-container {
  flex: 1;
  padding: 16px;
  overflow: hidden;
  min-height: 0; /* 关键：使Monaco容器可撑满并允许内部滚动 */
}

.code-editor {
  height: 100%;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow: auto;
  background: #2d3748;
}

.code-editor pre {
  margin: 0;
  padding: 16px;
  font-family: 'Courier New', 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  line-height: 1.5;
  color: #e2e8f0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0; /* 关键：使子元素正确参与flex高度计算 */
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;  /* 在此启用滚动 */
  min-height: 0;     /* 关键：允许在父容器内滚动 */
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  word-wrap: break-word;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.message-main {
  white-space: pre-wrap;
}

.message-loading {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #909399;
}

.message-stats {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
}

.bubble-user {
  background: #409eff;
  color: #fff;
  border-radius: 20px;
  border-bottom-right-radius: 10px;
}

.bubble-assistant {
  background: #f5f7fa;
  color: #303133;
  border: 1px solid #ebeef5;
  border-radius: 20px;
  border-bottom-left-radius: 10px;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.input-row {
  display: grid;
  grid-template-columns: 1fr 96px;
  gap: 12px;
  align-items: end;
}

.send-btn {
  height: 36px;
}

.input-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.file-dialog-content {
  display: flex;
  height: 400px;
}

.file-tree {
  flex: 1;
  border-right: 1px solid #e4e7ed;
  padding-right: 16px;
  overflow-y: auto;
}

.file-preview {
  flex: 1;
  padding-left: 16px;
}

.file-preview h4 {
  margin: 0 0 16px 0;
  color: #303133;
}

.file-info p {
  margin: 8px 0;
  color: #606266;
}

.tree-node {
  display: flex;
  align-items: center;
  gap: 8px;
}

.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* 记忆对话框样式 */
.memory-content {
  padding: 12px 0;
}

.memory-content .el-input__wrapper {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.6;
}

/* 路径浏览器样式 */
.path-browser {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.breadcrumbs {
  padding: 8px 0;
  border-bottom: 1px solid #e4e7ed;
}

.save-as-bar {
  padding: 12px 0;
  border-top: 1px solid #e4e7ed;
}

/* 安全检查弹窗样式 */
.security-report {
  padding: 8px 0;
}

.security-summary {
  margin-bottom: 20px;
}

.summary-text {
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 8px;
}

.summary-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.security-section {
  margin-bottom: 16px;
  border: 1px solid #ebeef5;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 15px;
}

.section-content {
  padding: 4px 0;
}

.details-text {
  margin: 0 0 12px 0;
  color: #606266;
  line-height: 1.6;
  font-size: 14px;
}

.issues-alert {
  margin-top: 12px;
}

.issues-list {
  margin: 8px 0;
  padding-left: 20px;
  list-style-type: disc;
}

.issues-list li {
  margin: 6px 0;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 1400px) {
  .panel-header {
    padding: 12px 16px;
  }
  
  .chat-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .chat-actions .el-select {
    width: 100%;
    margin-bottom: 8px;
    order: -1; /* 让下拉框排在第一个，单独一行 */
    flex-basis: 100%;
  }
  
  .chat-actions .el-button {
    flex: 0 1 auto; /* 按钮自适应宽度 */
  }
}

@media (max-width: 1200px) {
  .generator-content {
    grid-template-columns: 50% 6px 50% !important;
  }
  
  .panel-header h3 {
    font-size: 15px;
  }
  
  .chat-actions .el-button {
    font-size: 13px;
    padding: 8px 12px;
  }
}

@media (max-width: 768px) {
  .generator-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px 16px;
  }
  
  .generator-header h2 {
    font-size: 18px;
    margin-bottom: 12px;
  }
  
  .header-actions {
    width: 100%;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .header-actions .el-button {
    flex: 1;
    min-width: calc(50% - 4px);
  }
  
  .generator-content {
    height: calc(100vh - 180px) !important;
    grid-template-columns: 100% !important;
    grid-template-rows: 50% 6px 50%;
    overflow-y: auto;
  }
  
  .splitter {
    width: 100%;
    height: 6px;
    cursor: row-resize;
  }
  
  .editor-panel, .chat-panel {
    margin: 4px;
    min-height: 300px;
  }
  
  .panel-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 12px 16px;
  }
  
  .panel-header h3 {
    font-size: 14px;
    margin-bottom: 8px;
  }
  
  .editor-actions, .chat-actions {
    width: 100%;
    justify-content: center;
  }
  
  .chat-actions .el-button {
    flex: 1 1 calc(50% - 4px); /* 每行两个按钮 */
    min-width: 100px;
    max-width: 150px;
  }
  
  .message-content {
    max-width: 90%;
  }
}

@media (max-width: 480px) {
  .generator-header h2 {
    font-size: 16px;
  }
  
  .header-actions .el-button {
    font-size: 12px;
  }
  
  .panel-header h3 {
    font-size: 13px;
  }
  
  .message-content {
    max-width: 95%;
    font-size: 14px;
  }
  
  .input-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .send-btn {
    width: 100%;
  }
  
  .chat-actions .el-button {
    flex: 1 1 100%; /* 小屏幕上每个按钮占满一行 */
    max-width: none;
  }
  
  .editor-actions .el-button {
    font-size: 12px;
    padding: 6px 10px;
  }
}
</style>