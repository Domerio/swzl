<template>
  <div class="statistics">
    <h1>数据统计与可视化</h1>
    <h2>高频丢失物品类型</h2>
    <ul>
      <li v-for="item in frequentLostItems" :key="item.category__name">
        {{ item.category__name }} - {{ item.count }} 次
      </li>
    </ul>
    <h2>常见丢失地点</h2>
    <ul>
      <li v-for="location in commonLostLocations" :key="location.location">
        {{ location.location }} - {{ location.count }} 次
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      frequentLostItems: [],
      commonLostLocations: []
    }
  },
  mounted() {
    this.fetchStatistics()
  },
  methods: {
    async fetchStatistics() {
      try {
        const [frequentItemsRes, commonLocationsRes] = await Promise.all([
          axios.get('/api/statistics/frequent-lost-items/'),
          axios.get('/api/statistics/common-lost-locations/')
        ])
        this.frequentLostItems = frequentItemsRes.data
        this.commonLostLocations = commonLocationsRes.data
      } catch (error) {
        this.$message.error('获取统计数据失败，请稍后重试。')
      }
    }
  }
}
</script>

<style scoped>

</style>