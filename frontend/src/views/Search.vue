<template>
  <div class="search">
    <h1>失物招领信息搜索</h1>
    <el-input
        v-model="keyword"
        placeholder="请输入关键词（如“黑色钱包”）"
        @keyup.enter.native="search"
    ></el-input>
    <el-button @click="search">搜索</el-button>
    <ul>
      <li v-for="result in searchResults" :key="result.id">
        {{ result.title }} - {{ result.get_status_display() }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      keyword: '',
      searchResults: []
    }
  },
  methods: {
    async search() {
      try {
        const response = await axios.get('/api/search/', { params: { keyword: this.keyword } })
        this.searchResults = response.data
      } catch (error) {
        this.$message.error('搜索失败，请稍后重试。')
      }
    }
  }
}
</script>

<style scoped>

</style>