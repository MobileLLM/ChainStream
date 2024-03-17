import  request  from "@/utils/request"

export function getAgents() {
  return request({
    url: '/agents',
    method: 'get'
  })
}