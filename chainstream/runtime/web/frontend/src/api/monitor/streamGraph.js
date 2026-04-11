import request from '@/utils/request'

export function getStreamGraphData(params) {
  return request({
    url: '/monitor/streamGraph',
    method: 'get',
    params
  })
}

