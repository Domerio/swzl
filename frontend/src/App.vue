<!--frontend/src/App.vue-->
<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
  created() {
    this.$router.onError((error) => {
      console.error('全局路由错误捕获:', error)
      this.$message.error('页面加载失败，请检查网络连接')
    })
  }
}
</script>

<style>

#app {
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  overflow-y: auto;
}
body {
  margin: 0;
  overflow-x: hidden;
}
/* 解决ElementUI默认边距 */
.el-card {
  margin: 0 !important;
}
.el-form-item {
  margin-bottom: 18px;
}

</style>
