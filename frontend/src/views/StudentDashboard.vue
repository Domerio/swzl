<!--frontend/src/views/StudentDashboard.vue-->
<template>
  <div class="dashboard-container">
    <!-- 安全渲染层 -->
    <el-alert
      v-if="error"
      :title="error"
      type="error"
      show-icon
      class="error-alert"
    />

    <template v-if="!loading && !error">
      <!-- 个人信息卡 -->
      <el-card shadow="hover" class="user-card">
        <template #header>
          <span class="card-title">👤 我的信息</span>
        </template>
        <div class="user-info">
          <div class="info-item">
            <span class="label">姓名：</span>
            <el-tag type="success">{{ userInfo.name }}</el-tag>
          </div>
          <div class="info-item">
            <span class="label">学号：</span>
            <el-tag>{{ userInfo.id }}</el-tag>
          </div>
        </div>
      </el-card>

      <!-- 功能导航 -->
      <el-row :gutter="20" class="function-grid">
        <el-col :span="8">
          <el-card shadow="hover" class="function-card">
            <router-link to="/items/lost">
              <h3>📝 失物登记</h3>
              <p class="desc">丢失物品登记入口</p>
            </router-link>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="function-card">
            <router-link to="/items/found">
              <h3>🔍 招领查询</h3>
              <p class="desc">查看最新招领信息</p>
            </router-link>
          </el-card>
        </el-col>
      </el-row>
    </template>

    <!-- 加载状态 -->
    <div v-else class="loading-wrapper">
      <el-icon class="loading-icon" :size="50">
        <Loading />
      </el-icon>
      <p>正在加载学生数据...</p>
    </div>
  </div>
</template>


<script>
export default {
  data: () => ({
    loading: true,
    error: null,
    studentData: null
  }),

  computed: {
    // 计算属性安全访问用户信息
    userInfo() {
      return {
        name: this.$store.state.user.real_name || '未知用户',
        role: this.$store.state.user.role || '未定义角色',
        id: this.$store.state.user.id || '无ID'
      }
    }
  },

  async created() {
    await this.verifyAccess()
    await this.loadStudentData()
  },

  methods: {
    // 访问验证方法
    async verifyAccess() {
      if (!this.$store.state.user.isAuthenticated) {
        await this.$router.replace(`/login?redirect=${encodeURIComponent(this.$route.fullPath)}`)
        return
      }

      if (this.$store.state.user.role !== 'student') {
        this.$message.warning('非法访问学生页面')
        this.$router.go(-1)
        // return
      }
    },

    // 加载学生数据
    async loadStudentData() {
      try {
        const res = await this.$axios.get(`/api/students/${this.userInfo.id}/`)
        this.studentData = res.data
      } catch (error) {
        this.error = error.response?.data?.detail || '数据加载失败'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.user-card {
  margin-bottom: 20px;
  background: linear-gradient(145deg, #f8f9fa, #ffffff);
}

.card-title {
  font-size: 1.2em;
  font-weight: bold;
}

.user-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.label {
  font-weight: 500;
  margin-right: 8px;
  color: #606266;
}

.function-grid {
  margin-top: 30px;
}

.function-card {
  transition: transform 0.3s ease;
  cursor: pointer;
}

.function-card:hover {
  transform: translateY(-5px);
}

a {
  color: inherit;
  text-decoration: none;
}

.desc {
  color: #909399;
  font-size: 0.9em;
  margin-top: 8px;
}

.loading-wrapper {
  text-align: center;
  padding: 100px 0;
}

.loading-icon {
  animation: rotate 2s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.error-alert {
  margin: 20px 0;
}
</style>

