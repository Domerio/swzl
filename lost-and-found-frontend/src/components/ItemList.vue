<template>
  <div>
    <el-input
      v-model="searchKeyword"
      placeholder="输入关键词搜索"
      @keyup.enter="searchItems"
    ></el-input>
    <el-button @click="searchItems">搜索</el-button>
    <el-table :data="itemList" stripe>
      <el-table-column prop="itemName" label="物品名称"></el-table-column>
      <el-table-column prop="location" label="地点"></el-table-column>
      <el-table-column prop="status" label="状态"></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchKeyword: '',
      itemList: []
    };
  },
  methods: {
    searchItems() {
      // 这里发送搜索请求到后端，根据关键词过滤数据
      console.log('搜索关键词:', this.searchKeyword);
    }
  }
};
</script>