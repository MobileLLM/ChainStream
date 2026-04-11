import request from "@/utils/request.js";

export function getStatistics() {
  return request({
    url: "/monitor/statistics",
    method: "get"
  });
}
