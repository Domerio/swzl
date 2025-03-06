<!-- HomePage.vue -->
<el-menu :default-active="activeMenu">
  <template v-if="userInfo.role === 'student'">
    <el-menu-item index="found-items">失物信息</el-menu-item>
    <el-menu-item index="my-claims">我的申报</el-menu-item>
  </template>

  <template v-if="userInfo.role === 'admin'">
    <el-menu-item index="users">用户管理</el-menu-item>
    <el-menu-item index="audit">审核管理</el-menu-item>
  </template>
</el-menu>
