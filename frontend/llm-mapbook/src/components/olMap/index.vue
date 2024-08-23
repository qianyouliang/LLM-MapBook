<template>
  <div class="map-container">
    <div class="map-controls">
      <el-select v-model="selectedTile" placeholder="选择地图底图" @change="changeTileLayer">
        <el-option label="OpenStreetMap" value="osm"></el-option>
        <el-option label="Bing Maps" value="bing"></el-option>
        <el-option label="Stamen Terrain" value="stamen-terrain"></el-option>
      </el-select>
    </div>
    <div id="map" class="map"></div>
  </div>
</template>
<script>
import 'ol/ol.css'; // 确保样式正确导入
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import OSM from 'ol/source/OSM';
import XYZ from 'ol/source/XYZ';
import BingMaps from 'ol/source/BingMaps';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import Style from 'ol/style/Style';
import CircleStyle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import { fromLonLat } from 'ol/proj';
import Vue from 'vue';
import { FullScreen, ScaleLine, ZoomSlider } from 'ol/control'; // 导入控件

export default {
  data() {
    return {
      map: null,
      vectorSource: new VectorSource(),
      selectedTile: 'osm', // 默认选择OpenStreetMap
      tileLayer: null,
    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      // 初始化地图
      this.tileLayer = new TileLayer({
        source: new OSM(),
      });

      this.map = new Map({
        target: "map",
        layers: [
          this.tileLayer,
          new VectorLayer({
            source: this.vectorSource,
            style: new Style({
              image: new CircleStyle({
                radius: 5,
                fill: new Fill({
                  color: "red",
                }),
              }),
            }),
          }),
        ],
        view: new View({
          center: fromLonLat([0, 0]),
          zoom: 2,
        }),
        controls: [
          new FullScreen(), // 全屏控件
          new ScaleLine(), // 比例尺控件
          new ZoomSlider(), // 缩放滑块控件
        ],
      });

      // 将地图实例存储在 Vue 原型上，以便全局访问
      Vue.prototype.$map = this.map;
    },
    changeTileLayer() {
      let newSource;
      switch (this.selectedTile) {
        case 'osm':
          newSource = new OSM();
          break;
        case 'bing':
          newSource = new BingMaps({
            key: 'Your-Bing-Maps-Key', // 请替换为你的Bing Maps API Key
            imagerySet: 'Road',
          });
          break;
        case 'stamen-terrain':
          newSource = new XYZ({
            url: 'http://tile.stamen.com/terrain/{z}/{x}/{y}.jpg',
          });
          break;
        // 其他地图源可以在这里添加
        default:
          newSource = new OSM();
      }
      this.tileLayer.setSource(newSource);
    },
    updateMap(coordinates) {
      // 更新地图上的标记
      this.vectorSource.clear();
      coordinates.forEach((coord) => {
        const feature = new Feature({
          geometry: new Point(fromLonLat(coord)),
        });
        this.vectorSource.addFeature(feature);
      });
    },
  },
};
</script>


<style lang="less" scoped>
.map-container {
  position: relative;
  width: 56vw;
  height: 48vh;
}

.map-controls {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 1000;
  background-color: white;
  padding: 5px;
  border-radius: 4px;
}

.map {
  width: 100%;
  height: 100%;
}
</style>
