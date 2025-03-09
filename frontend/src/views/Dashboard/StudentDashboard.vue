<template>
  <div class="student-dashboard">
    <el-container>
      <el-header>
        <h2>学生仪表板</h2>
        <el-button type="danger" @click="handleLogout">退出登录</el-button>
      </el-header>
      
      <el-main>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="box-card">
              <div slot="header">
                <span>个人信息</span>
              </div>
              <div class="user-info">
                <p><strong>学号：</strong>{{ user.username }}</p>
                <p><strong>姓名：</strong>{{ user.name }}</p>
                <p><strong>身份：</strong>学生</p>
              </div>
            </el-card>
          </el-col>
          
          <el-col :span="16">
            <el-card class="box-card">
              <div slot="header">
                <span>快捷操作</span>
              </div>
              <div class="quick-actions">
                <el-button type="primary" @click="handleLostItem">登记失物</el-button>
                <el-button type="success" @click="handleFoundItem">登记招领</el-button>
                <el-button type="info" @click="handleSearch">搜索物品</el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'StudentDashboard',
  computed: {
    ...mapGetters(['currentUser']),
    user() {
      return this.currentUser || {}
    }
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    },
    handleLostItem() {
      // 实现失物登记功能
      this.$message.info('失物登记功能开发中...')
    },
    handleFoundItem() {
      // 实现招领登记功能
      this.$message.info('招领登记功能开发中...')
    },
    handleSearch() {
      // 实现搜索功能
      this.$message.info('搜索功能开发中...')
    }
  }
}
</script>

<style scoped>
.student-dashboard {
  height: 100vh;
  background-color: #f0f2f5;
}

.el-header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12);
}

.el-main {
  padding: 20px;
}

.box-card {
  margin-bottom: 20px;
}

.user-info p {
  margin: 10px 0;
}

.quick-actions {
  display: flex;
  gap: 10px;
}

.quick-actions .el-button {
  flex: 1;
}
</style> 