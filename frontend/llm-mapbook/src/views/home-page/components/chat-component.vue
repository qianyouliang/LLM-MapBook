<template>
  <div class="chat">
    <el-card class="chat-area">
      <div slot="header" class="clearfix">MapAgent
        <div class="tool-bar">

        </div>
      </div>
      <div class="chat-container">
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
        <el-button @click="sendMessage"><img src="/image/page-icon/submit.png" alt="" class="submit-icon"></el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chatHistory: [],
      userInput: "",
      username: "GISer Liu",
    };
  },
  mounted() {},
  methods: {
    handleKeydown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault(); // 阻止默认的换行行为
        this.sendMessage();
      }
    },
    sendMessage() {
      // 检查输入是否为空或仅包含空格
      if (!this.userInput.trim()) {
        return;
      }
      const id = 'user_'+new Date().getTime();
      this.chatHistory.push({ id: id, role: "user", content: this.userInput });
      // 模拟回复
      setTimeout(() => {
        const id = 'role_'+new Date().getTime();
        this.chatHistory.push({ id: id, role: "AI", content: "这是AI的回复" });
      }, 1000);
      this.userInput = "";
    },
  },
};
</script>

<style lang="less" scoped>
.chat {
  width: 100%;
  height: 40vh;

  .chat-area {
    height: 100%;
    position: relative;
    .chat-container {
      height: 200px;
      overflow-y: auto;
      margin-bottom: 10px;
    }
    .user-input {
      position: absolute;
      bottom: 20px;
      width: 96%;
      display: flex;
      justify-content: center;
      align-content: center;
      ::v-deep .el-textarea__inner {
        height: 35px !important;
        font-size: 14px;
        font-weight: bold;
      }
      ::v-deep .el-button {
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        

        .submit-icon{
            
            width: 16px;
            height: 16px;
        }
      }
    }
  }

  .chat-message {
    margin-bottom: 30px;
  }
}
</style>