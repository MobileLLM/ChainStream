import { createI18n } from 'vue-i18n'
import zhCN from './locales/zh-CN'
import enUS from './locales/en-US'

// 从 localStorage 获取保存的语言设置，默认为中文
const savedLanguage = localStorage.getItem('language') || 'zh-CN'

const i18n = createI18n({
  legacy: false, // 使用 Composition API 模式
  locale: savedLanguage,
  fallbackLocale: 'en-US',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  }
})

export default i18n
