<template>
  <div class="lost-item-list">
    <h1>失物信息列表</h1>
    <ul>
      <li v-for="item in lostItems" :key="item.id">
        {{ item.title }} - {{ item.get_status_display() }}
        <el-button @click="updateStatus(item.id, 'completed', 'returned')">标记为已归还</el-button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      lostItems: []
    }
  },
  mounted() {
    this.fetchLostItems()
  },
  methods: {
    async fetchLostItems() {
      try {
        const response = await axios.get('/api/items/lost/')
        this.lostItems = response.data
      } catch (error) {
        this.$message.error('获取失物信息失败，请稍后重试。')
      }
    },
    async updateStatus(itemId, status, result) {
      try {
        const response = await axios.post(`/api/items/${itemId}/update-status/`, { status, result })
        this.$message.success('信息状态已更新')
        this.fetchLostItems()
      } catch (error) {
        this.$message.error('更新状态失败，请稍后重试。')
      }
    }
  }
}
</script>

<style scoped>

</style>