<template>
  <div id="map" class="map"></div>
</template>

<script>
import 'ol/ol.css'; // 确保样式正确导入
import Map from 'ol/Map';
import View from 'ol/View';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import Style from 'ol/style/Style';
import CircleStyle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import { fromLonLat } from 'ol/proj';
import Vue from 'vue';
export default {
  data() {
    return {
      map: null,
      vectorSource: new VectorSource(),
    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      this.map = new Map({
        target: "map",
        layers: [
          new TileLayer({
            source: new OSM(),
          }),
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
      });
      Vue.prototype.$map = this.map;
    },
    
    updateMap(coordinates) {
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
.map {
  width: 100%;
  height: 100%;
}
</style>
