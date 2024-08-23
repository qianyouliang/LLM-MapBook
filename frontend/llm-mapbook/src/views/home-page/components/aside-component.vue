<template>
  <div class="aside-component">
    <el-menu mode="horizontal" class="aside-menu">
      <el-menu-item index="1" @click="toggleTab('settings')">
        应用设置
      </el-menu-item>
      <el-menu-item index="2" @click="toggleTab('intro')"
        >项目介绍
      </el-menu-item>
    </el-menu>
    <div v-if="currentTab === 'settings'" class="tab-container">
      <div class="settle-container">
        <div class="settle-item">
          <div class="settle-title">模型类型：</div>
          <el-select v-model="localModelType" placeholder="选择模型类型">
            <el-option label="deepseek" value="deepseek"></el-option>
            <el-option label="ipex_llm" value="ipex_llm"></el-option>
          </el-select>
        </div>
        <div class="settle-item">
          <div class="settle-title">API_KEY：</div>
          <el-input
            v-if="localModelType === 'deepseek'"
            v-model="localApiKey"
            placeholder="请输入deepseek_key"
            show-password
          />
        </div>
        <div class="settle-item">
          <div class="settle-title">地理编码类型：</div>
          <el-select v-model="localGeocodeType" placeholder="地理编码类型">
            <el-option label="free" value="free"></el-option>
            <el-option label="baidu" value="baidu"></el-option>
          </el-select>
        </div>
        <div class="settle-item">
          <div class="settle-title">
            {{ localGeocodeType === "baidu" ? "百度地图API" : "用户名" }}:
          </div>
          <el-input
            v-if="localGeocodeType === 'baidu'"
            v-model="localBaiduKey"
            placeholder="请输入百度地图API"
            show-password
          />
          <el-input v-else v-model="localUsername" placeholder="请输入用户名" />
        </div>
      </div>
      <div class="settle-item">
        <div class="settle-title">文件上传：</div>
        <el-upload
          class="upload-demo"
          drag
          action="https://jsonplaceholder.typicode.com/posts/"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :file-list="fileList"
          :on-change="handleFileChange"
          :auto-upload="false"
          multiple
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">拖拽文件或<em>点击上传</em></div>
          <div class="el-upload__tip" slot="tip">PDF或TXT格式</div>
        </el-upload>
      </div>
    </div>
    <div v-else class="tab-container">
      <div v-html="parsedMarkdown"></div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";

export default {
  data() {
    return {
      currentTab: "settings",
      localUsername: "",
      localModelType: "",
      localApiKey: "",
      localGeocodeType: "",
      localBaiduKey: "",
      markdownContent:
        "## AI-MapBook \nAI-MapBook是一个利用大型语言模型（LLM）技术为故事讲述提供地图支持的项目。它通过LLM从书籍中提取地理信息和属性信息，结合地理编码得到地理坐标数据，并在交互式地图上进行可视化展示，为读者提供沉浸式的故事探索体验。\n```代码展示```",
    };
  },
  computed: {
    ...mapState("user", [
      "username",
      "modelType",
      "apiKey",
      "geocodeType",
      "baiduKey",
    ]),
    parsedMarkdown() {
      return marked(this.markdownContent);
    },
  },
  watch: {
    localUsername(newVal) {
      this.SET_USER_NAME(newVal);
    },
    localModelType(newVal) {
      this.SET_MODEL_TYPE(newVal);
    },
    localApiKey(newVal) {
      this.SET_API_KEY(newVal);
    },
    localGeocodeType(newVal) {
      this.SET_GEOCODE_TYPE(newVal);
    },
    localBaiduKey(newVal) {
      this.SET_BAIDU_MAP_API(newVal);
    },
  },
  methods: {
    ...mapMutations("user", [
      "SET_USER_NAME",
      "SET_MODEL_TYPE",
      "SET_API_KEY",
      "SET_GEOCODE_TYPE",
      "SET_BAIDU_MAP_API",
    ]),
    toggleTab(tabName) {
      this.currentTab = tabName;
    },
    handleFileChange(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.processFileContent(e.target.result);
      };
      reader.readAsText(file.raw);
    },
    processFileContent(content) {
      getEventList(content, this.modelType, this.apiKey).then((events) => {
        this.events = events;
      });
    },
    truncatedTitle(title) {
      return title.length > 6 ? title.substring(0, 6) + "..." : title;
    },
  },
  created() {
    // Initialize local data with state values
    this.localUsername = this.username;
    this.localModelType = this.modelType;
    this.localApiKey = this.apiKey;
    this.localGeocodeType = this.geocodeType;
    this.localBaiduKey = this.baiduKey;
  },
};
</script>

<style lang="less" scoped>
.aside-component {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  .aside-menu {
    position: absolute;
    top: 1vh;
    width: 100%;
    padding: 1vh 0.5vw;
  }
  .tab-container {
    position: absolute;
    top: 10vh;
    width: 100%;
    height: 60vh;
    padding: 1vh 0.5vw 1vh 0.5vw;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    .settle-item {
      width: 350px;
      min-height: 50px;
      height: auto;
      padding-left: 120px;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      position: relative;
      .settle-title {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        left: 0.5vw;

        width: 120px;
        font-size: 16px;
        font-weight: bold;
        color: #000;
      }
    }
  }
}
::v-deep .el-input,
.el-input__inner {
  width: 250px;
}
</style>