import axios from "axios";

export function getEventList(content, modelType, apiKey) {
  return axios.post("/api/get_event_list", {
    content,
    modelType,
    apiKey,
  });
}

export function processEvent(event, geocodeType, apiKey, baiduKey) {
  return axios.post("/api/process_event", {
    event,
    geocodeType,
    apiKey,
    baiduKey,
  });
}
