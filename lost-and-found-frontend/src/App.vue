<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <el-menu default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose">
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-menu"></i> 用户系统</template>
            <el-menu-item index="1-1">用户注册/登录</el-menu-item>
            <el-menu-item index="1-2">个人中心</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i> 失物与招领信息管理</template>
            <el-menu-item index="2-1">失物登记</el-menu-item>
            <el-menu-item index="2-2">招领登记</el-menu-item>
            <el-menu-item index="2-3">信息列表</el-menu-item>
          </el-submenu>
          <el-menu-item index="3"><i class="el-icon-message"></i> 消息通知</el-menu-item>
          <el-menu-item index="4"><i class="el-icon-data-analysis"></i> 数据统计与可视化</el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-main>
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>