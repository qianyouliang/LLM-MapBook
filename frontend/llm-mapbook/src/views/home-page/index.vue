<template>
  <div class="home-page">
    <div class="left-panel">
      <el-card class="full-height-card">
        <div slot="header" class="clearfix">
          <span>阅读框</span>
        </div>
        <el-input
          type="textarea"
          :rows="35"
          placeholder="粘贴文本或上传文件"
          v-model="textInput"
        >
        </el-input>
        <el-row type="flex" justify="start" class="button-row">
          <el-col :span="8">
            <el-upload
              class="upload-demo"
              action="/your-backend-endpoint"
              :on-change="handleFileChange"
              :auto-upload="false"
            >
              <el-button size="small" type="primary">点击上传</el-button>
            </el-upload>
          </el-col>
          <el-col :span="8">
            <el-button size="small" type="primary" @click="submitText"
              >提交</el-button
            >
          </el-col>
          <el-col :span="8">
            <el-button size="small" type="primary" @click="showMap"
              >展示</el-button
            >
          </el-col>
        </el-row>
      </el-card>
    </div>
    <div class="right-panel">
      <h2>地图页面</h2>
      <Map />
    </div>
  </div>
</template>

<script>
import Map from "@/components/olMap/index.vue";
import { getGeojsonData } from "@/api/index.js";
export default {
  data() {
    return {
      textInput: "",
    };
  },
  components: {
    Map,
  },
  mounted() {},
  methods: {
    handleFileChange(file, fileList) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.textInput = e.target.result;
      };
      reader.readAsText(file.raw);
    },
    submitText() {
      // 这里可以调用后端API处理文本并获取地理坐标
      // 假设获取到的坐标为 [[lon1, lat1], [lon2, lat2], ...]
      const coordinates = [
        [116.4074, 39.9042],
        [121.4737, 31.2304],
      ]; // 示例坐标
      this.updateMap(coordinates);
    },
    submitUpload() {
      if (!this.file) {
        this.$message.warning("请先选择文件");
        return;
      }
      const formData = new FormData();
      formData.append("file", this.file);
      this.getGeojsonData(formData);
    },
    showMap() {
      // 展示地图的逻辑
    },
  },
};
</script>

<style>
.home-page {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}
.left-panel {
  flex: 1;
  padding: 0.5vw;
  height: 100%;
  background-color: #f0f0f0;
}
.right-panel {
  flex: 2;
  padding: 0.5vw;
  height: 100%;
}
.full-height-card {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
.full-height-card .el-card__body {
  flex: 1;
  overflow: auto;
}
.button-row {
  margin-top: 10px;
}
</style>