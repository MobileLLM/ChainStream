import request from '@/utils/request.js'

export function checkConnection() {
    return request({
        url: '/home/checkConnection',
        method: 'get'
    })
}