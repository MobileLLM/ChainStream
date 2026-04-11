import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import * as echarts from 'echarts'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'highlight.js/styles/github.css'
// import router from './router/index.js'
import router from './router'
import i18n from './i18n'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}


app.use(ElementPlus)
app.use(router)
app.use(i18n)
// app.use(router)
app.config.globalProperties.$echarts = echarts
app.mount('#app')
