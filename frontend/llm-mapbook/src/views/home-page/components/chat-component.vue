<template>
  <div class="chat">
    <el-card class="chat-area">
      <div slot="header" class="clearfix">MapAgent</div>
      <div class="chatContainer">
        <div class="tool-bar">
          <el-checkbox v-model="useRAG">RAG<i class="heading-icon" :class="{'el-icon-loading': isRAG === false, 'el-icon-success': isRAG ===true}"></i></el-checkbox>
          <el-checkbox v-model="useSmartMap">智能地图</el-checkbox>
          
        </div>
        <div v-for="msg in chatHistory" :key="msg.id" class="chat-message">
          <strong>{{ msg.role }}:</strong> {{ msg.content }}
        </div>
      </div>
      <div class="user-input">
        <el-input
          type="textarea"
          v-model="userInput"
          placeholder="你想聊点什么?"
          @keydown.native="handleKeydown"
        >
        </el-input>
        <el-button @click="sendMessage"
          ><img src="/image/page-icon/submit.png" alt="" class="submit-icon"
        /></el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
// import { getChatMessage } from "@/api/index.js";
export default {
  data() {
    return {
      chatHistory: [],
      userInput: "",
      useRAG: false,
      useSmartMap: false,
    };
  },
  computed: {
    ...mapState("user", [
      "username",
      "modelType",
      "apiKey",
      "geocodeType",
      "baiduKey",
      "isRAG",
    ]),
    ...mapState("user", ["eventList"]),
  },
  mounted() {},
  methods: {
    ...mapMutations("user", ["SET_CHAT_CONFIG"]),
    handleKeydown(event) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // 阻止默认的换行行为
        this.sendMessage();
      }
    },
    sendMessage() {
      // 检查输入是否为空或仅包含空格
      if (!this.userInput.trim()) {
        return;
      }
      console.log("userInput:", this.userInput);
      console.log("modelType:", this.modelType);
      console.log("apiKey:", this.apiKey);
      console.log("useRAG:", this.useRAG);
      const id = "user_" + new Date().getTime();
      this.chatHistory.push({ id: id, role: "user", content: this.userInput });
      
      // 构建 JSON 对象
      let jsonData = {
        message: this.userInput,
        model_type: this.modelType,
        api_key: this.apiKey,
        use_rag: this.useRAG,
        is_ragged: this.isRAG,
      };
      
      this.chat(jsonData);
    },
    async chat(data) {
      this.userInput = "";
      const response = await fetch("/api/chat", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let responseContent = "";
      const id = "role_" + new Date().getTime();

      // 读取流式响应数据
      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          break;
        }
        const text = decoder.decode(value, { stream: true });
        responseContent = text;

        // 每次接收到数据都更新 chatHistory
        this.chatHistory = this.chatHistory.map((msg) =>
          msg.id === id ? { ...msg, content: responseContent } : msg
        );

        // 如果消息不存在则添加一条新的消息
        if (!this.chatHistory.some((msg) => msg.id === id)) {
          this.chatHistory.push({
            id: id,
            role: "AI",
            content: responseContent,
          });
        }
      }

      console.log("Stream ended");
      
    },
  },
};
</script>

<style lang="less" scoped>
.scrollbar(@width, @track-bg, @thumb-bg, @thumb-hover-bg) {
  &::-webkit-scrollbar {
    width: @width;
  }

  &::-webkit-scrollbar-track {
    background: @track-bg;
  }

  &::-webkit-scrollbar-thumb {
    background-color: @thumb-bg;
    border-radius: @width / 2;
  }

  &::-webkit-scrollbar-thumb:hover {
    background-color: @thumb-hover-bg;
  }
}
.chat {
  width: 100%;
  height: 100%;
  background-color: #424242;
  color: #fff;
  position: relative;
  .chat-area {
    height: 99.5%;

    background-color: #424242 !important;
    color: #fff;
    overflow-y: scroll;
    // 应用滚动条样式
    .scrollbar(2px, #424242, #888, #555);
    .chatContainer {
      height: auto;
      overflow-y: auto;
      margin-bottom: 10px;
      // 应用滚动条样式

    }
    .clearfix {
      width: 100%;
      height: 55px;
      display: flex;
      align-items: center;
      padding-left: 20px;
      font-weight: bold;
      font-size: 16px;

      background-color: #424242;
      position: absolute;
      left: 0;
      top: 0;
    }
    .tool-bar {
      position: absolute;
      right: 40px;
      top: 15px;
      .heading-icon{
        position: absolute;
        top: 2px;
        left: -20px;
        font-size: 14px;
        color: rgb(40, 231, 40);
      }
    }
    .user-input {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      width: 90%;
      padding: 0 10px;
      display: flex;
      justify-content: flex-start;
      align-content: center;
      ::v-deep .el-textarea__inner {
        height: 35px !important;
        font-size: 14px;
        font-weight: bold;
      }
      ::v-deep .el-button {
        height: 35px;
        width: 35px;
        display: flex;
        align-items: center;
        justify-content: center;

        .submit-icon {
          width: 16px;
          height: 16px;
        }
      }
    }
  }

  .chat-message {
    margin-bottom: 30px;
    color: #fff;
    height: auto;
  }
}
::v-deep .el-checkbox__label,
.el-checkbox__label {
  color: #fff !important;
}
</style>