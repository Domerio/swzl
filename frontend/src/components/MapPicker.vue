<!-- MapPicker.vue -->
<template>
  <div id="map-container" style="height: 400px; width: 100%"></div>
</template>

<script>
export default {
  props: ['initialLat', 'initialLng'],
  methods: {
    initMap() {
      const map = new AMap.Map('map-container', {
        zoom: 15,
        center: [this.initialLng || 116.397428, this.initialLat || 39.90923]
      });
      map.on('click', (e) => {
        this.$emit('update:initialLat', e.lnglat.getLat());
        this.$emit('update:initialLng', e.lnglat.getLng());
      });
    }
  },
  mounted() {
    if (!window.AMap) {
      const key = '你的高德地图API Key';
      const script = document.createElement('script');
      script.src = `https://webapi.amap.com/maps?v=1.4.15&key=${key}`;
      script.onload = this.initMap;
      document.head.appendChild(script);
    } else {
      this.initMap();
    }
  }
};
</script>