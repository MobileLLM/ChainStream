import  request  from "@/utils/request"

export function getAgentsPath() {
  return request({
    url: '/monitor/agents',
    method: 'get'
  })
}

export function startAgent(agentId) {
  return request({
    url: '/monitor/agents/start/' + agentId,
    method: 'post'
  })
}

export function stopAgent(agentId) {
  return request({
    url: '/monitor/agents/stop/' + agentId,
    method: 'post'
  })
}

export function getRunningAgents() {
  return request({
    url: '/monitor/agents/getRunningAgents',
    method: 'get'
  })
}
