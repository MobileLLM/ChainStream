import  request  from "@/utils/request"

export function getDeviceCards() {
  return request({
    url: '/devices/deviceCards',
    method: 'get'
  })
}

export function getAgentList() {
  return request({
    url: '/devices/agentList',
    method: 'get'
  })
}

export function checkDevice(device_form) {
  return request({
    url: '/devices/checkDevice',
    method: 'post',
    data: device_form
  })
}

export function addDevice(device_form) {
  return request({
    url: '/devices/addDevice',
    method: 'post',
    data: device_form,
  })
}

