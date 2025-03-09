<script setup>

</script>

<template>
  <div class="admin-dashboard">
    <h1>管理员控制台 - 欢迎 {{ user.real_name }}</h1>
    <!-- 管理员特定功能模块 -->
    <el-button @click="$router.push('/admin/found-items')">查看失物信息</el-button>

  </div>
</template>

<script>
export default {
  name: 'AdminDashboard'
}
</script>

<style scoped>

</style>