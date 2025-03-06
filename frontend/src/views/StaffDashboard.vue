<script setup>

</script>

<template>
  <div class="staff-dashboard">
    <h1>工作人员控制台 - 欢迎 {{ user.real_name }}</h1>
    <!-- 工作人员特定功能模块 -->
    <el-button @click="$router.push('/staff/found-items')">查看失物信息</el-button>
  </div>

</template>

<script>
export default {
  name: 'StaffDashboard'
}
</script>


<style scoped>

</style>