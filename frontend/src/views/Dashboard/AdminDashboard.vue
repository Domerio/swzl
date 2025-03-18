<template>
  <div class="admin-dashboard">
    <h1>管理员控制台 - 欢迎 {{ user.real_name }}</h1>
    <!-- 统计信息展示 -->
    <el-row :gutter="20">
      <!-- 待审核信息数量 -->
      <el-col :span="8">
        <el-card class="status-card">
          <div class="status-content">
            <i class="status-icon el-icon-time"></i>
            <div class="status-info">
              <h3 class="status-title">待审核信息</h3>
              <p class="status-count">{{ pendingCount }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 进行中信息数量 -->
      <el-col :span="8">
        <el-card class="status-card">
          <div class="status-content">
            <i class="status-icon el-icon-circle-check"></i>
            <div class="status-info">
              <h3 class="status-title">进行中信息</h3>
              <p class="status-count">{{ activeCount }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
      <!-- 已完成信息数量 -->
      <el-col :span="8">
        <el-card class="status-card">
          <div class="status-content">
            <i class="status-icon el-icon-check"></i>
            <div class="status-info">
              <h3 class="status-title">已完成信息</h3>
              <p class="status-count">{{ completedCount }}</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 管理员特定功能模块 -->
    <el-row :gutter="20" class="data-section">
      <!-- 查看失物信息 -->
      <el-col :span="12">
        <el-card>
          <div slot="header" class="card-header">
            <span>查看失物信息</span>
            <el-button
                type="text"
                @click="$router.push('/admin/found-items')">
              查看全部 <i class="el-icon-arrow-right"></i>
            </el-button>
          </div>
          <el-table
              :data="recentPosts"
              @row-click="handleRowClick"
              class="clickable-table">
            <el-table-column
                prop="title"
                label="标题"
                min-width="120">
            </el-table-column>
            <el-table-column
                prop="category"
                label="分类"
                width="100">
            </el-table-column>
            <el-table-column
                label="状态"
                width="100">
              <template slot-scope="scope">
                <el-tag :type="statusTypeMap[scope.row.status]" size="small">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <!-- 查看用户信息 -->
      <el-col :span="12">
        <el-card>
          <div slot="header" class="card-header">
            <span>查看用户信息</span>
            <el-button
                type="text"
                @click="$router.push('/admin/users')">
              查看全部 <i class="el-icon-arrow-right"></i>
            </el-button>
          </div>
          <el-table
              :data="recentUsers"
              @row-click="handleUserRowClick"
              class="clickable-table">
            <el-table-column
                prop="username"
                label="学号/工号"
                min-width="120">
            </el-table-column>
            <el-table-column
                prop="real_name"
                label="真实姓名"
                width="100">
            </el-table-column>
            <el-table-column
                prop="role"
                label="角色"
                width="100">
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';

// import dayjs from 'dayjs';

export default {
  data() {
    return {
      user: {
        real_name: '加载中...'
      },
      pendingCount: 0,
      activeCount: 0,
      completedCount: 0,
      recentPosts: [],
      recentUsers: [],
      statusTypeMap: {
        pending: 'warning',
        active: 'primary',
        completed: 'success',
        expired: 'info'
      }
    };
  },
  mounted() {
    this.fetchAdminData();
  },
  methods: {
    async fetchAdminData() {
      try {
        const config = {
          headers: {
            Authorization: `Token ${localStorage.getItem('token')}` // 添加token验证
          }
        };

        // 获取用户信息
        const userResponse = await axios.get('/api/user/profile/', config);
        this.user = userResponse.data;

        // 获取失物招领信息统计
        const statsResponse = await axios.get('/api/admin/stats/', config);
        this.pendingCount = statsResponse.data.pending_count;
        this.activeCount = statsResponse.data.active_count;
        this.completedCount = statsResponse.data.completed_count;

        // 获取最近的失物招领信息
        const postsResponse = await axios.get('/api/admin/recent-posts/', config);
        this.recentPosts = postsResponse.data.recent_posts;

        // 获取最近的用户信息
        const usersResponse = await axios.get('/api/admin/recent-users/', config);
        this.recentUsers = usersResponse.data.recent_users;
      } catch (error) {
        console.error('Error fetching admin data:', error);
        this.$message.error('获取数据失败: ' + error.response?.data?.message || error.message);
      }
    },

    handleRowClick(row) {
      // 处理失物招领信息行点击事件
      this.$router.push(`/admin/found-items/${row.id}`);
    },
    handleUserRowClick(row) {
      // 处理用户信息行点击事件
      this.$router.push(`/admin/users/${row.id}`);
    }
  }
};
</script>

<style scoped lang="scss">
.admin-dashboard {
  padding: 20px;
}

.status-card {
  text-align: center;
}

.status-icon {
  font-size: 36px;
  color: #909399;
  margin-bottom: 10px;
}

.status-title {
  font-size: 16px;
  color: #303133;
}

.status-count {
  font-size: 24px;
  color: #606266;
  margin-top: 5px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>