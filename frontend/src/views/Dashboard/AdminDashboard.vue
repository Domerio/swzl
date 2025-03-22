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
                  class="view-more">
              </el-button>
            </div>
          </template>

          <el-table
              :data="recentPosts"
              @row-click="handleRowClick"
              class="data-table"
              empty-text="暂无待处理信息"
              v-loading="loading.posts"
              :header-cell-style="{ background: '#f8f9fa' }"
              height="330"
          >
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
            <el-table-column label="类型" width="100">
              <template #default="{row}">
                {{ getItemTypeLabel(row.item_type) }}
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
                  class="view-more">
              </el-button>
            </div>
          </template>
          <el-table
              :data="recentUsers"
              @row-click="handleUserRowClick"
              class="data-table"
              v-loading="loading.users"
              :header-cell-style="{ background: '#f8f9fa' }"
              height="330"
          >
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

    <!-- 物品详情弹窗 -->
    <el-dialog title="📦 物品详情" :visible.sync="itemDialogVisible" width="800px" class="admin-detail-dialog">
      <el-row :gutter="20">
        <!-- 添加图片轮播区 -->
        <el-col :span="8">
          <el-carousel :interval="5000" height="300px" arrow="always">
            <el-carousel-item v-for="(img, index) in currentItem.images"
                              :key="index">
              <el-image
                  :src="img"
                  :preview-src-list="currentItem.images"
                  fit="cover"
                  class="detail-image">
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
            </el-carousel-item>
          </el-carousel>
        </el-col>

        <!-- 调整信息展示区 -->
        <el-col :span="16">
          <el-descriptions :column="2" border label-class-name="detail-label">
            <el-descriptions-item label="物品名称">{{ currentItem.title }}</el-descriptions-item>
            <el-descriptions-item label="分类">{{ currentItem.category }}</el-descriptions-item>
            <el-descriptions-item label="发布类型">
              {{ currentItem.item_type === 'lost' ? '失物登记' : '招领登记' }}
            </el-descriptions-item>

            <el-descriptions-item label="丢失时间">{{ formatTime(currentItem.lost_time) }}</el-descriptions-item>
            <el-descriptions-item label="丢失地点">
              {{ currentItem.location }}
              <!-- 添加地图容器 -->
              <div
                  v-if="currentItem.location_lat && currentItem.location_lng"
                  class="detail-map-container"
                  :id="'detail-map-' + currentItem.id"
              ></div>
            </el-descriptions-item>
            <el-descriptions-item label="提交人">
              <el-tooltip
                  v-if="currentItem.user?.role === 'admin'"
                  content="管理员账号">
                <i class="el-icon-s-custom"></i>
              </el-tooltip>
              {{ currentItem.user?.real_name || '匿名用户' }}
              <span v-if="currentItem.user" class="user-role-tag">
                ({{ roleMap[currentItem.user.role] }})
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="statusTypeMap[currentItem.status]">{{ currentItem.status }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="联系方式" :span="2">
              <el-link type="primary">{{ currentItem.contact }}</el-link>
            </el-descriptions-item>
            <el-descriptions-item label="详细描述" :span="2">
              <pre class="description-pre">{{ currentItem.description }}</pre>
            </el-descriptions-item>
          </el-descriptions>
        </el-col>
      </el-row>

      <!-- 添加底部操作按钮 -->
      <div slot="footer">
        <el-button @click="itemDialogVisible = false">关闭</el-button>
        <el-button
            v-if="currentItem.status === 'pending'"
            type="success"
            :disabled="!currentItem.id || approvalProcessing"
            @click="handleApproveItem"
            :loading="approvalProcessing">
          {{ approvalProcessing ? '正在处理...' : '审核通过' }}
        </el-button>

      </div>
    </el-dialog>


    <!-- 用户详情弹窗 -->
    <el-dialog
        title="👤 用户详情"
        :visible.sync="userDialogVisible"
        width="600px"
        class="admin-detail-dialog">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ currentUser.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ currentUser.real_name }}</el-descriptions-item>
        <el-descriptions-item label="用户角色">
          <el-tag :type="roleTagType(currentUser.role)">{{ currentUser.role }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ currentUser.date_joined }}</el-descriptions-item>
        <el-descriptions-item label="最后登录">{{ currentUser.last_login }}</el-descriptions-item>
        <el-descriptions-item label="联系方式">{{ currentUser.phone }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ currentUser.email }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

  </div>

</template>


<script>
import axios from 'axios';
import dayjs from "dayjs";

// import dayjs from 'dayjs';

export default {
  /* eslint-disable no-undef */
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
      },
      // 新增弹窗控制状态
      itemDialogVisible: false,
      userDialogVisible: false,
      currentItem: {},
      currentUser: {},

    };
  },
  computed: {
    roleMap() {
      return {
        admin: '管理员',
        teacher: '教职工',
        student: '学生'
      }
    }

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
    if (!window.AMap) {
      const key = 'db70318a1cf1f196b2746f10cb9df826'
      const plugins = [
        'AMap.Scale',
        'AMap.ToolBar'
      ].join(',')
      const script = document.createElement('script')
      script.src = `https://webapi.amap.com/maps?v=2.0&key=${key}&plugin=${plugins}`
      script.onerror = () => {
        console.error('高德地图SDK加载失败')
      }
      document.head.appendChild(script)
    }
  },
  methods: {
    // 初始化详情地图
    // 修改initDetailMap方法
    initDetailMap() {
      if (!window.AMap) {
        this.$message.warning('地图资源正在加载，请稍候')
        return
      }

      // 确保数据有效性
      const lng = parseFloat(this.currentItem.location_lng)
      const lat = parseFloat(this.currentItem.location_lat)
      if (isNaN(lng) || isNaN(lat)) {
        console.warn('无效的经纬度数据', this.currentItem)
        return
      }

      // 使用nextTick确保DOM更新
      this.$nextTick(() => {
        try {
          this.destroyDetailMap()

          const mapContainerId = `detail-map-${this.currentItem.id}`
          const mapContainer = document.getElementById(mapContainerId)
          if (!mapContainer) return

          // 初始化地图
          this.detailMap = new AMap.Map(mapContainerId, {
            zoom: 17,
            center: new AMap.LngLat(lng, lat),
            resizeEnable: true,
            viewMode: '3D'
          })

          // 添加控件
          const tools = [
            new AMap.Scale(),
            new AMap.ToolBar({
              position: {bottom: '20px', right: '20px'}
            })
          ]
          tools.forEach(t => t.addTo(this.detailMap))

          // 添加标记
          new AMap.Marker({
            position: new AMap.LngLat(lng, lat),
            content: '<div class="detail-marker">📍</div>',
            map: this.detailMap
          })
        } catch (e) {
          console.error('地图初始化失败:', e)
          this.$message.error('地图加载失败，请检查网络连接')
        }
      })
    },
    // 销毁地图
    // 修改destroyDetailMap方法
    destroyDetailMap() {
      if (this.detailMap) {
        try {
          // 清除所有覆盖物
          this.detailMap.clearMap()
          // 销毁地图实例
          this.detailMap.destroy()
          // 移除DOM元素
          const container = this.detailMap.getContainer()
          if (container && container.parentNode) {
            container.parentNode.removeChild(container)
          }
        } catch (e) {
          console.warn('地图销毁异常:', e.message)
        }
        this.detailMap = null
      }
    },
    getItemTypeLabel(type) {
      return type === 'lost' ? '失物' : '招领';
    },
    getCategoryName(categoryId) {
      return axios.get(`/api/category/name/${categoryId}/`)
          .then(response => response.data.name)
          .catch(() => '未知分类');
    },
    formatTime(time) {
      return dayjs(time).format('YYYY-MM-DD HH:mm')
    },
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
      } catch (error) {
        console.error('Error:', error);
        this.$message.error(error.response?.data?.message || '数据加载失败');
      } finally { // 确保最终清除加载状态
        this.loading = {posts: false, users: false};
      }
    },
    // 物品详情
    async handleRowClick(row) {
      try {
        const apiUrl = `/api/admin/found-items/${row.id}/`;
        const response = await axios.get(apiUrl, {
          headers: {Authorization: `Token ${localStorage.getItem('token')}`}
        });
        // 新增：获取分类名称并合并到数据
        const categoryName = await this.getCategoryName(response.data.category);
        this.currentItem = {
          ...response.data,
          category: categoryName,  // 用分类名称替换原始ID值
          images: response.data.images || [],
          user: response.data.user || {}
        };
        this.itemDialogVisible = true;
      } catch (error) {
        this.$message.error('获取详情失败');
      }
    },
    // 用户详情展示
    async handleUserRowClick(row) {
      try {
        const response = await axios.get(`/api/admin/users/${row.id}/`, {
          headers: {Authorization: `Token ${localStorage.getItem('token')}`}
        });
        this.currentUser = response.data;
        this.userDialogVisible = true;

        // 处理日期格式
        this.currentUser.date_joined = new Date(this.currentUser.date_joined)
            .toLocaleString();
        this.currentUser.last_login = this.currentUser.last_login
            ? new Date(this.currentUser.last_login).toLocaleString()
            : '从未登录';
      } catch (error) {
        this.$message.error('获取用户详情失败');
        console.error('Error fetching user details:', error);
      }
    },
    // 审核通过
    async handleApproveItem() {
      try {
        // 强校验物品状态
        if (this.currentItem.status !== 'pending') {
          throw new Error('只能审核待处理状态的物品')
        }
        await this.$confirm('确定要通过该物品的审核吗？', '操作确认', {
          confirmButtonClass: 'el-button--danger' // 使用危险按钮样式
        });
        const startTime = Date.now()
        await this.$http.patch(
            `/admin/items/${this.currentItem.id}/status/`, // 使用专用状态接口
            {
              status: 'active',
              admin_remark: '已通过审核' // 添加审核备注
            },
            {
              headers: {
                'X-Request-ID': `approve-req-${this.currentItem.id}-${Date.now()}`, // 唯一请求标识
                'Content-Type': 'application/json-patch+json' // 标准PATCH类型
              }
            }
        )
        // 执行本地数据更新
        this.currentItem = {
          ...this.currentItem,
          status: 'active',
          admin_remark: '已通过审核'
        }
        // 更新统计数字
        this.pendingCount--
        this.activeCount++
        // 更新表格数据
        this.recentPosts = this.recentPosts.map(item =>
            item.id === this.currentItem.id ?
                {...item, status: 'active'} :
                item
        )
        console.log(`审核操作耗时 ${Date.now() - startTime}ms`)
        this.$message.success(`${this.currentItem.title} 审核通过`)
      } catch (error) {
        const isCancel = error === 'cancel'
        const msg = isCancel ? '操作已取消' :
            error.response?.data?.error || `审核失败: ${error.message}`

        !isCancel && console.error('审核错误详情:', {
          error: error.response?.data,
          item: this.currentItem
        })

        this.$message[isCancel ? 'info' : 'error'](msg)
      }
    },
  },
  // 添加watch监听对话框状态
  watch: {
    itemDialogVisible(newVal) {
      if (newVal) {
        // 添加延迟确保DOM渲染完成
        setTimeout(() => {
          this.initDetailMap()
        }, 300)
      } else {
        this.destroyDetailMap()
      }
    },
    // 监听当前物品变化
    currentItem: {
      deep: true,
      handler() {
        if (this.itemDialogVisible) {
          this.$nextTick(() => {
            this.initDetailMap()
          })
        }
      }
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

.welcome-title {
  margin: 0;
}

.admin-detail-dialog {
  .el-carousel {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

    &__arrow {
      background-color: rgba(255, 255, 255, 0.5);

      &:hover {
        background-color: rgba(255, 255, 255, 0.8);
      }
    }

    .detail-image {
      width: 100%;
      height: 300px;
      border-radius: 4px;
    }

    .no-image {
      height: 300px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #909399;
      font-size: 16px;
      background: #f8f9fa;
    }
  }

  .image-error {
    background: #f8f9fa;
    display: flex;
    align-items: center;
    justify-content: center;

    i {
      font-size: 40px;
      color: #DCDFE6;
    }
  }

  .description-pre {
    white-space: pre-wrap;
    line-height: 1.6;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 4px;
    margin: 0;
    font-family: inherit;
  }

  .detail-label {
    width: 100px;

    ::after {
      content: '';
    }
  }
}

// 新增样式规则
.user-role-tag {
  color: #909399;
  font-size: 12px;
  margin-left: 6px;
}

.image-error {
  background: #f8f9fa;
  @apply flex items-center justify-center;

  i {
    @apply text-4xl text-gray-300;
  }
}

// 添加详情地图样式
.detail-map-container {
  width: 100%;
  height: 200px;
  margin-top: 12px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;

  &::after {
    content: '高德地图提供支持';
    position: absolute;
    right: 5px;
    bottom: 5px;
    font-size: 10px;
    color: #666;
    background: rgba(255, 255, 255, 0.8);
    padding: 2px 5px;
    border-radius: 3px;
  }
}

// 标记点样式
.detail-marker {
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: translate(-12px, -24px);
}
</style>