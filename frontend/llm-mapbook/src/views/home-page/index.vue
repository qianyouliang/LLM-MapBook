<template>
  <div class="home-page">
    <el-container
      style="height: 100%; margin: 0; overflow: hidden; border: 1px solid #000"
    >
      <!-- <el-aside width="20%" style="overflow: hidden !important; height:100vh !important;border:1px solid #000;">
          
        </el-aside> -->
      <el-drawer title="应用设置" :visible.sync="drawer" :with-header="false">
        <Aside />
      </el-drawer>

      <!-- 主内容区 -->
      <el-main
        style="
          overflow: hidden !important;
          height: 100vh !important;
          border: 1px solid #000;
          
        "
      >
        <el-row class="header">
          <div class="tool-bar">
            <div class="settle" @click="drawer = true">
              <i class="el-icon-setting"></i>
            </div>
          </div>
        </el-row>
        <el-row :gutter="10" class="map-container">
          <el-col :span="6" class="event-container">
            <el-card class="event-list">
              <div slot="header" class="clearfix">事件列表</div>
              <div
                v-for="event in eventList"
                :key="event.id"
                class="event-item"
              >
                <el-tooltip
                  class="item"
                  effect="dark"
                  :content="event.title"
                  placement="top"
                >
                  <span>{{ truncatedTitle(event.title) }}</span>
                </el-tooltip>
                <el-button @click="showEvent(event)">查看</el-button>
              </div>
            </el-card>
          </el-col>
          <el-col :span="18" class="map">
            <el-card class="map-area">
              <Map ref="mapComponent" />
            </el-card>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <Chat />
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Map from "@/components/olMap/index.vue";
import Chat from "./components/chat-component.vue";
import Aside from "./components/aside-component.vue";
import { getEventList, processEvent } from "@/api/index.js";

export default {
  name: "Home",
  components: {
    Map,
    Chat,
    Aside,
  },
  data() {
    return {
      eventList: [],
      drawer: false,
    };
  },
  computed: {
    parsedMarkdown() {
      return marked(this.markdownContent);
    },
  },
  methods: {
    showEvent(event) {
      processEvent(event, this.geocodeType, this.apiKey, this.baiduKey).then(
        (processedEvent) => {
          this.$refs.mapComponent.addMarker(processedEvent);
        }
      );
    },
  },
};
</script>

<style lang="less" scoped>
.home-page {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;

  align-items: center;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #424242;

  * {
    overflow-y: hidden;
  }
}
.header{
  width: 100%;
  height: 40px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 10px;
  margin-bottom: 10px;
  position: relative;
  .settle {
  position: absolute;
  top: 1vh;
  right: 1.5vw;
}
}

.map-container {
  display: flex;
  width: 100%;
  border: 1px solid #000;
  .map{
    padding: 0 !important;
    margin:0;
  }
}
.event-list,
.map-area {
  height: 50vh;
}

.event-item {
  margin-bottom: 10px;
}
</style>
