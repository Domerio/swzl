<template>
  <div class="admin-dashboard">
    <!-- 头部区域 -->
    <div class="dashboard-header">
      <div class="header-content">
        <div>
          <h1 class="welcome-title">欢迎回来，{{ user.real_name }}！👋</h1>

        </div>
        <el-button
          type="danger"
          plain
          @click="handleLogout"
          class="logout-btn"
          icon="el-icon-switch-button">
          退出登录
        </el-button>
      </div>
      <p class="welcome-sub">今日有 {{ pendingCount }} 项待处理事务</p>
    </div>

    <!-- 数据概览卡片 -->
    <el-row :gutter="24" class="metric-grid">
      <el-col :xs="24" :sm="12" :lg="8">
        <el-card class="metric-card metric-pending" shadow="hover">
          <div class="metric-content">
            <div class="metric-icon">
              <i class="el-icon-time"></i>
            </div>
            <div class="metric-info">
              <span class="metric-label">待审核</span>
              <span class="metric-value">{{ pendingCount }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="8">
        <el-card class="metric-card metric-active" shadow="hover">
          <div class="metric-content">
            <div class="metric-icon">
              <i class="el-icon-loading"></i>
            </div>
            <div class="metric-info">
              <span class="metric-label">进行中</span>
              <span class="metric-value">{{ activeCount }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :lg="8">
        <el-card class="metric-card metric-completed" shadow="hover">
          <div class="metric-content">
            <div class="metric-icon">
              <i class="el-icon-success"></i>
            </div>
            <div class="metric-info">
              <span class="metric-label">已完成</span>
              <span class="metric-value">{{ completedCount }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <!-- 数据表格区域 -->
    <el-row :gutter="24" class="data-grid">
      <el-col :xs="24" :lg="12">
        <el-card class="data-card" shadow="never">
          <template #header>
            <div class="card-header">
              <div class="header-title">
                <i class="el-icon-box"></i>
                <span>最新失物信息</span>
              </div>
              <el-button
                  type="text"
                  class="view-more"
                  @click="$router.push('/admin/found-items')">
                管理全部 <i class="el-icon-arrow-right"></i>
              </el-button>
            </div>
          </template>

          <el-table
              :data="recentPosts"
              @row-click="handleRowClick"
              class="data-table"
              empty-text="暂无待处理信息"
              v-loading="loading.posts"
              :header-cell-style="{ background: '#f8f9fa' }">
            <!--添加空插槽-->
            <template #empty>
              <div class="empty-state">
                <i class="el-icon-document-remove"></i>
                <span>当前没有可显示的失物信息</span>
              </div>
            </template>
            <el-table-column prop="title" label="物品名称" min-width="180">
              <template #default="{row}">
                <span class="text-ellipsis">{{ row.title }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="category" label="分类" width="120">
              <template #default="{row}">
                <el-tag effect="plain">{{ row.category }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
              <template #default="{row}">
                <el-tag
                    :type="statusTypeMap[row.status]"
                    effect="light"
                    class="status-tag">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="12">
        <el-card class="data-card" shadow="never">
          <template #header>
            <div class="card-header">
              <div class="header-title">
                <i class="el-icon-user"></i>
                <span>新增用户</span>
              </div>
              <el-button
                  type="text"
                  class="view-more"
                  @click="$router.push('/admin/users')">
                管理全部 <i class="el-icon-arrow-right"></i>
              </el-button>
            </div>
          </template>
          <el-table
              :data="recentUsers"
              @row-click="handleUserRowClick"
              class="data-table"
              v-loading="loading.users"
              :header-cell-style="{ background: '#f8f9fa' }">
            <el-table-column prop="username" label="学工号" min-width="120">
              <template #default="{row}">
                <div class="user-cell">
                  <el-avatar :size="24" :src="row.avatar || defaultAvatar">
                    {{ row.real_name?.charAt(0) || '?' }}
                  </el-avatar>
                  <span>{{ row.username || '无数据' }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="real_name" label="姓名" width="100"/>
            <el-table-column prop="role" label="角色" width="100">
              <template #default="{row}">
                <el-tag
                    :type="roleTagType(row.role)"
                    effect="light"
                    class="role-tag">
                  {{ row.role }}
                </el-tag>
              </template>
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
        real_name: '加载中...',
        avatar: require('@/assets/touxiang.jpg'),
        role: '',
        phone: ''
      },
      defaultAvatar: require('@/assets/touxiang.jpg'),
      pendingCount: 0,
      activeCount: 0,
      completedCount: 0,
      recentPosts: [],
      recentUsers: [],
      loading: {
        posts: true,
        users: true
      },
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
    this.$nextTick(() => {
      const observer = new MutationObserver(() => {
        const loadingElements = document.querySelectorAll('.el-loading-mask');
        loadingElements.forEach(el => {
          if (el.style.display !== 'none') {
            setTimeout(() => el.style.display = 'none', 5000); // 异常情况下最多展示5秒
          }
        });
      });

      observer.observe(this.$el, {
        childList: true,
        subtree: true
      });
    });
  },
  methods: {
    // 退出登录
    handleLogout() {
      this.$confirm('确定要退出系统吗？', '操作确认', {
        type: 'warning',
        confirmButtonText: '确认退出',
        cancelButtonText: '取消'
      }).then(() => {
        this.$store.dispatch('logout')
        this.$router.replace('/login')
        this.$message.success('已安全退出系统')
      }).catch(() => {
      })
    },
    roleTagType(role) {
      const roleTypes = {
        admin: 'danger',
        teacher: 'warning',
        student: 'success'
      };
      return roleTypes[role] || 'info';
    },
    async fetchAdminData() {
      try {
        this.loading = {posts: true, users: true} // 重置加载状态
        const config = {
          headers: {Authorization: `Token ${localStorage.getItem('token')}`}
        };
        // 并行请求优化
        const [userResp, statsResp, postsResp, usersResp] = await Promise.all([
          axios.get('/api/user/profile/', config),
          axios.get('/api/admin/stats/', config),
          axios.get('/api/admin/recent-posts/', config),
          axios.get('/api/admin/recent-users/', config)
        ]);
        // 数据赋值
        this.user = userResp.data;
        this.pendingCount = statsResp.data.pending_count;
        this.activeCount = statsResp.data.active_count;
        this.completedCount = statsResp.data.completed_count;
        this.recentPosts = postsResp.data.recent_posts;
        this.recentUsers = usersResp.data.recent_users;
        console.log(this.recentUsers)
      } catch (error) {
        console.error('Error:', error);
        this.$message.error(error.response?.data?.message || '数据加载失败');
      } finally { // 确保最终清除加载状态
        this.loading = {posts: false, users: false};
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
  padding: 24px;
  background: #f8fafc;
  min-height: 100vh;
}

.dashboard-header {
  margin-bottom: 12px;
  position: relative;
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
}
.logout-btn {
  padding: 10px 16px;
  border-radius: 8px;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
  }

  i {
    margin-right: 8px;
  }
}


.metric-grid {
  margin-bottom: 24px;

  .metric-card {
    margin-bottom: 24px;
    border: 0;
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-2px);
    }

    .metric-content {
      display: flex;
      align-items: center;
      padding: 20px;

      .metric-icon {
        width: 56px;
        height: 56px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 16px;

        i {
          font-size: 28px;
          color: white;
        }
      }

      .metric-info {
        display: flex;
        flex-direction: column;

        .metric-label {
          color: #6b7280;
          font-size: 14px;
          margin-bottom: 4px;
        }

        .metric-value {
          font-size: 28px;
          font-weight: 600;
          color: #1a2b3c;
        }
      }
    }

    &.metric-pending {
      .metric-icon {
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
      }
    }

    &.metric-active {
      .metric-icon {
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
      }
    }

    &.metric-completed {
      .metric-icon {
        background: linear-gradient(135deg, #10b981, #34d399);
      }
    }
  }
}

.data-grid {
  .data-card {
    border-radius: 12px;

    ::v-deep .el-card__header {
      padding: 16px 24px;
      background: #f8f9fa;
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      color: #1a2b3c;
      font-weight: 500;

      i {
        font-size: 18px;
      }
    }

    .view-more {
      padding: 8px;
      color: #6b7280;

      &:hover {
        color: #3b82f6;
      }
    }
  }

  .data-table {
    border-radius: 8px;

    ::v-deep th {
      font-weight: 500;
    }

    .user-cell {
      display: flex;
      align-items: center;
      gap: 12px;

      .user-avatar {
        flex-shrink: 0;
      }
    }

    .status-tag, .role-tag {
      border-radius: 4px;
      font-weight: 500;
    }

    .text-ellipsis {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      display: inline-block;
      max-width: 200px;
    }
  }
}

@media (max-width: 768px) {
  .dashboard-header {
    .header-content {
      flex-direction: column;
      gap: 16px;
    }
  }

  .logout-btn {
    width: 100%;
    justify-content: center;
  }
}


::v-deep .el-loading-mask {
  background-color: rgba(255, 255, 255, 0.8);

  .el-loading-spinner {
    .circular {
      width: 42px;
      height: 42px;
    }

    .el-loading-text {
      font-weight: 500;
      color: #4b5563;
    }
  }
}
.welcome-title{
  margin: 0px;
}
</style>