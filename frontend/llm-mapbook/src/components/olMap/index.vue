<template>
  <div class="map-container">
    <div class="map-controls">
      <el-select
        v-model="selectedTile"
        placeholder="选择地图底图"
        @change="changeTileLayer"
      >
        <el-option label="OpenStreetMap" value="osm"></el-option>
        <el-option label="ArcGIS Terrain" value="arcgis-terrain"></el-option>
        <el-option label="高德地图" value="gaode"></el-option>
        <el-option label="Google地图" value="google"></el-option>
        <el-option label="Google影像" value="googleImage"></el-option>
        <el-option label="ArcGIS" value="arcgis"></el-option>
        <el-option label="ArcGIS影像" value="arcgisImage"></el-option>
      </el-select>
    </div>
    <div id="map" class="map"></div>
    <div id="popup" class="ol-popup">
      <a href="#" id="popup-closer" class="ol-popup-closer"></a>
      <div id="popup-content"></div>
    </div>
  </div>
</template>

<script>
import "ol/ol.css"; // 确保样式正确导入
import Map from "ol/Map";
import View from "ol/View";
import TileLayer from "ol/layer/Tile";
import VectorLayer from "ol/layer/Vector";
import OSM from "ol/source/OSM";
import XYZ from "ol/source/XYZ";
import VectorSource from "ol/source/Vector";
import Feature from "ol/Feature";
import Point from "ol/geom/Point";
import LineString from "ol/geom/LineString";
import Overlay from "ol/Overlay";
import Style from "ol/style/Style";
import CircleStyle from "ol/style/Circle";
import Fill from "ol/style/Fill";
import Stroke from "ol/style/Stroke";
import Text from "ol/style/Text";
import { fromLonLat } from "ol/proj";
import Vue from "vue";
import { FullScreen, ScaleLine, ZoomSlider } from "ol/control"; // 导入控件

export default {
  data() {
    return {
      map: null,
      vectorSource: new VectorSource(),
      selectedTile: "osm", // 默认选择OpenStreetMap
      tileLayer: null,
      overlay: null,
      locations: [],
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
            style: (feature) => {
              return new Style({
                image: new CircleStyle({
                  radius: 5,
                  fill: new Fill({ color: "red" }),
                }),
                stroke: new Stroke({
                  color: feature.get("strokeColor") || "blue",
                  width: 2,
                }),
                text: new Text({
                  text: feature.get("name"),
                  font: "12px Calibri,sans-serif",
                  fill: new Fill({ color: "black" }),
                  stroke: new Stroke({
                    color: "white",
                    width: 3,
                  }),
                }),
              });
            },
          }),
        ],
        view: new View({
          center: fromLonLat([0, 0]),
          zoom: 2,
        }),
        controls: [new FullScreen(), new ScaleLine(), new ZoomSlider()],
      });

      // Popup for point features
      this.overlay = new Overlay({
        element: document.getElementById("popup"),
        autoPan: true,
        autoPanAnimation: {
          duration: 250,
        },
      });
      this.map.addOverlay(this.overlay);

      const closer = document.getElementById("popup-closer");
      closer.onclick = () => {
        this.overlay.setPosition(undefined);
        closer.blur();
        return false;
      };

      // 点击事件
      this.map.on("singleclick", this.handleMapClick);

      // 将地图实例存储在 Vue 原型上，以便全局访问
      Vue.prototype.$map = this.map;
    },
    changeTileLayer() {
      let newSource;
      switch (this.selectedTile) {
        // 地图图层切换
        case "osm":
          newSource = new OSM();
          break;
        case "google":
          newSource = new XYZ({
            url: "http://mt2.google.cn/vt/lyrs=m@167000000&hl=zh-CN&gl=cn&x={x}&y={y}&z={z} ",
            wrapX: false,
          });
          break;
        case "googleImage":
          newSource = new XYZ({
            url: "http://mt3.google.cn/vt/lyrs=s&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}",
            wrapX: false,
          });
          break;
        case "arcgis-terrain":
          newSource = new XYZ({
            url: "https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
          });
          break;
        case "gaode":
          newSource = new XYZ({
            url: "http://wprd0{1-4}.is.autonavi.com/appmaptile?lang=zh_cn&size=1&style=7&x={x}&y={y}&z={z}",
            wrapX: false,
          });
          break;
        case "gaodeImage":
          newSource = new XYZ({
            url: "http://mt3.google.cn/vt/lyrs=s&hl=zh-CN&gl=cn&x={x}&y={y}&z={z}",
            wrapX: false,
          });
          break;
        case "arcgis":
          newSource = new XYZ({
            url:
              "http://server.arcgisonline.com/ArcGIS/rest/services/" +
              "World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
          });
          break;
        case "arcgisImage":
          newSource = new XYZ({
            url:
              // 测试地址
              "https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          });
          break;
        // 其他地图源可以在这里添加
        default:
          newSource = new OSM();
      }
      this.tileLayer.setSource(newSource);
    },
    addMarker(info, coordinates) {
      try {
        // 添加点位
        const pointFeature = new Feature({
          geometry: new Point(fromLonLat([coordinates.longitude, coordinates.latitude])),
          name: info.event_title || "",
        });

        // 设置popup内容
        pointFeature.set("popupContent", `
          <div style="max-height: 200px; overflow-y: auto; font-size: 16px; line-height: 1.5;">
            <b>${info.event_title}</b><br>
            <strong>事件类型</strong>: ${info.event_type}<br>
            <strong>内容</strong>: ${info.event_content}<br>
            <strong>关键词</strong>: ${info.keys.join(", ")}
          </div>
        `);

        this.vectorSource.addFeature(pointFeature);
        this.locations.push(fromLonLat([coordinates.longitude, coordinates.latitude]));
      } catch (exc) {
        console.error(`Error adding marker: ${exc}`);
      }
    },
    addPolyline(color = "blue", weight = 2.5, opacity = 1, arrow = true) {
      if (this.locations.length > 1) {
        // 添加折线
        const lineFeature = new Feature({
          geometry: new LineString(this.locations),
        });

        lineFeature.set("strokeColor", color);
        this.vectorSource.addFeature(lineFeature);

        if (arrow) {
          // 为每段线添加箭头
          for (let i = 0; i < this.locations.length - 1; i++) {
            const dx = this.locations[i + 1][0] - this.locations[i][0];
            const dy = this.locations[i + 1][1] - this.locations[i][1];
            const angle = -Math.atan2(dy, dx) * 180 / Math.PI;

            const midLocation = [
              (this.locations[i][0] + this.locations[i + 1][0]) / 2,
              (this.locations[i][1] + this.locations[i + 1][1]) / 2,
            ];

            const arrowFeature = new Feature({
              geometry: new Point(midLocation),
            });

            arrowFeature.setStyle(new Style({
              image: new CircleStyle({
                radius: 5,
                fill: new Fill({ color }),
                stroke: new Stroke({
                  color,
                  width: weight,
                }),
              }),
              text: new Text({
                text: "→",
                font: `bold 12px Calibri,sans-serif`,
                fill: new Fill({ color }),
                stroke: new Stroke({
                  color: "white",
                  width: 2,
                }),
                textAlign: "center",
                offsetX: 0,
                offsetY: 10,
                rotation: angle * Math.PI / 180,
              }),
            }));

            this.vectorSource.addFeature(arrowFeature);
          }
        }
      }
    },
    handleMapClick(event) {
      // 处理点击事件
      const features = this.map.getFeaturesAtPixel(event.pixel);
      if (features.length > 0) {
        const feature = features[0];
        const coordinates = feature.getGeometry().getCoordinates();
        const content = feature.get("popupContent") || "无详细信息";

        const popupContent = document.getElementById("popup-content");
        popupContent.innerHTML = content;
        this.overlay.setPosition(coordinates);
      } else {
        this.overlay.setPosition(undefined);
      }
    },
    updateMap(features) {
      this.locations = [];
      this.vectorSource.clear();

      // 根据传入的特征信息添加点位和折线
      features.forEach((feature) => {
        if (feature.type === "Point") {
          this.addMarker(feature.properties.description, {
            longitude: feature.geometry.coordinates[0],
            latitude: feature.geometry.coordinates[1],
          });
        }
      });

      // 添加连接点位的折线
      this.addPolyline();
    },
  },
};
</script>


<style lang="less" scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 60vh;
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
.ol-popup {
  position: absolute;
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 10px;
  border: 1px solid #cccccc;
  bottom: 12px;
  left: -50px;
  min-width: 280px;
}

.ol-popup:after,
.ol-popup:before {
  top: 100%;
  border: solid transparent;
  content: " ";
  height: 0;
  width: 0;
  position: absolute;
  pointer-events: none;
}

.ol-popup:after {
  border-top-color: white;
  border-width: 10px;
  left: 48px;
  margin-left: -10px;
}

.ol-popup:before {
  border-top-color: #cccccc;
  border-width: 11px;
  left: 48px;
  margin-left: -11px;
}

.ol-popup-closer {
  text-decoration: none;
  position: absolute;
  top: 2px;
  right: 8px;
}
</style>
