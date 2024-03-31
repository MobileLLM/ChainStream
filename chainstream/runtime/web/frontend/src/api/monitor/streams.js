import request from "@/utils/request.js";

export function getStreams() {
  return request({
    url: "/monitor/streams",
    method: "get"
  });
}