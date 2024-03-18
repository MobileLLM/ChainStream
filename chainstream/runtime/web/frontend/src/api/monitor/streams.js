import request from "@/utils/request.js";

export function getStreams() {
  return request({
    url: "/api/monitor/streams",
    method: "get"
  });
}