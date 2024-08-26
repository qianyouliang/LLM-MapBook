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
        <el-row :gutter="10" >
          <el-col  class="chat-container">
            <Chat />
          </el-col>
          <el-col  class="event-container">
            <el-row class="map">
              <!-- <el-card class="map-area"> -->
              <Map ref="mapComponent" />
              <!-- </el-card> -->
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
            </el-row>
          </el-col>
        </el-row>
        <!-- <el-row>

        </el-row> -->
      </el-main>
    </el-container>
  </div>
</template>

<script>
import Map from "@/components/olMap/index.vue";
import Chat from "./components/chat-component.vue";
import Aside from "./components/aside-component.vue";


export default {
  name: "home-page",
  components: {
    Map,
    Chat,
    Aside,
  },
  data() {
    return {
      
      drawer: false,
    };
  },

  methods: {
    
  },
};
</script>

<style lang="less" scoped>
.home-page {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  * {
    color: #fff !important;
  }
  align-items: center;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  overflow: hidden;
  background-color: #424242;

  * {
    overflow-y: hidden;
     overflow-x: hidden;
  }
}
.header {
  width: 100%;
  height: 40px;
  background-color: #fff;
  border: 1px solid #000;
  border-radius: 10px;
  margin-bottom: 10px;
  position: relative;
  background-color: #424242;
  .settle {
    position: absolute;
    top: 1vh;
    right: 1.5vw;
  }
}

.chat-container {
  display: flex;
  width: 20%;
  height: 90vh;
  padding: 1vh 0.5vw;
  border: 1px solid #fff;
  background-color: #424242;
  overflow-x: hidden;
}

.event-container {
  width: 80%;
  height: 90vh;
  margin: 0;
  padding: 0;
  border:1px solid #fff;


  .map {
    width: 100%;
    height: 100%;
  }
  .event-list {
    margin-top: 1vh;
    height: 28vh;
    // width: 100%;
    background-color: #221919;
  }
}

.event-item {
  margin-bottom: 10px;
}
</style>
