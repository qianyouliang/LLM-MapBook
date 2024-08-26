import axios from "axios";

const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // FastAPI 后端服务地址
  withCredentials: false, // This is the default
});

// 文件上传
const fileUpload = (formData) => {
  return apiClient.post('/api/upload_file/', formData);
}

// 文件处理
const processFile = (formData) => {
  return apiClient.post("/api/process_file/", formData);
}

// 检查RAG构建状态
const checkRAGStatus = (file_id) => {
  return apiClient.get(`/api/check_rag_status/${file_id}`);
}

// 聊天Chat
const getChatMessage = async (data) => {
  const response = await axios.post('/api/chat/', data, {
    responseType: 'stream',
  });
  return response;
}

export {
  processFile,
  checkRAGStatus,
  getChatMessage,
  fileUpload,
}