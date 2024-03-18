import axios from 'axios';


axios.defaults.headers['Content-Type'] = 'application/json;charset=utf-8'
// 创建axios实例
const service = axios.create({
    // axios中请求配置有baseURL选项，表示请求URL公共部分
    baseURL: import.meta.env.VITE_CHAINSTREAM_BACKEND_API  + '/api/',
    // 超时
    timeout: 30000,
    // 禁用 Cookie 等信息
    withCredentials: false,
})
//
// service.interceptors.request.use(config => {
//     // get请求映射params参数
//     if (config.method === 'get' && config.params) {
//         let url = config.url + '?';
//         for (const propName of Object.keys(config.params)) {
//             const value = config.params[propName];
//             const part = encodeURIComponent(propName) + '='
//             if (value !== null && typeof(value) !== "undefined") {
//                 if (typeof value === 'object') {
//                     for (const key of Object.keys(value)) {
//                         let params = propName + '[' + key + ']';
//                         const subPart = encodeURIComponent(params) + '='
//                         url += subPart + encodeURIComponent(value[key]) + "&";
//                     }
//                 } else {
//                     url += part + encodeURIComponent(value) + "&";
//                 }
//             }
//         }
//         url = url.slice(0, -1);
//         config.params = {};
//         config.url = url;
//     }
//     return config
// }, error => {
//     console.log(error)
//     Promise.reject(error)
// })
//
// // 响应拦截器
// service.interceptors.response.use(async res => {
//         // 未设置状态码则默认成功状态
//         const code = res.data.code || 200;
//         // 获取错误信息
//         const msg = res.data.msg || errorCode[code] || errorCode['default']
//         if (ignoreMsgs.indexOf(msg) !== -1) { // 如果是忽略的错误码，直接返回 msg 异常
//             return Promise.reject(msg)
//         } else if (code === 500) {
//             Message({
//                 message: msg,
//                 type: 'error'
//             })
//             return Promise.reject(new Error(msg))
//         } else if (code === 501) {
//             Message({
//                 type: 'error',
//                 duration: 0,
//                 message: msg
//             })
//             return Promise.reject(new Error(msg))
//         } else if (code !== 200) {
//             if (msg === '无效的刷新令牌') { // hard coding：忽略这个提示，直接登出
//                 console.log(msg)
//             } else {
//                 Notification.error({
//                     title: msg
//                 })
//             }
//             return Promise.reject('error')
//         } else {
//             return res.data
//         }
//     }, error => {
//         console.log('err' + error)
//         let {message} = error;
//         if (message === "Network Error") {
//             message = "后端接口连接异常";
//         } else if (message.includes("timeout")) {
//             message = "系统接口请求超时";
//         } else if (message.includes("Request failed with status code")) {
//             message = "系统接口" + message.substr(message.length - 3) + "异常";
//         }
//         Message({
//             message: message,
//             type: 'error',
//             duration: 5 * 1000
//         })
//         return Promise.reject(error)
//     }
// )

export default service;
