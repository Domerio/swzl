<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 个人信息列 -->
      <el-col :span="6">
        <el-card class="user-card">
          <div class="user-info">
            <el-upload
                class="avatar-uploader"
                :action="uploadAction"
                :headers="uploadHeaders"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
                :method="requestMethod"
            name="file">
              <!--                :upload-avatar="uploadAvatar"-->
              <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" alt="">
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
            <h2 class="user-name">{{ userInfo.real_name || '未命名用户' }}</h2>
            <p class="user-role">{{ roleMap[userInfo.role] }}</p>

            <div class="stats-wrapper">
              <div class="stat-item">
                <span class="stat-number">{{ dashboardData.total_posts }}</span>
                <span class="stat-label">总发布</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ dashboardData.total_bookmarks }}</span>
                <span class="stat-label">总收藏</span>
              </div>
              <div class="stat-item">
                <span class="stat-number">{{ dashboardData.unread_notifications }}</span>
                <span class="stat-label">未读通知</span>
              </div>
            </div>

            <el-button
                type="primary"
                size="small"
                icon="el-icon-edit"
                @click="showEditDialog">
              修改资料
            </el-button>
          </div>
          <!-- 在用户信息卡片中添加 -->
          <el-button
              type="danger"
              size="small"
              icon="el-icon-switch-button"
              @click="handleLogout"
              style="margin-top: 15px;">
            安全退出
          </el-button>
        </el-card>

        <!-- 快捷操作区 -->
        <el-card class="quick-actions">
          <div slot="header" class="clearfix">
            <span>快捷功能</span>
          </div>
          <el-button
              type="primary"
              icon="el-icon-s-release"
              @click="$router.push('/lost-item/new')">
            失物登记
          </el-button>
          <el-button
              type="success"
              icon="el-icon-s-claim"
              @click="$router.push('/found-item/new')">
            招领登记
          </el-button>
        </el-card>
      </el-col>

      <!-- 主要内容区 -->
      <el-col :span="18">
        <el-row :gutter="20">
          <!-- 状态统计卡片 -->
          <el-col
              v-for="(count, status) in dashboardData.status_summary"
              :key="status"
              :span="8">
            <el-card class="status-card">
              <div class="status-content">
                <i :class="['status-icon', statusIconMap[status]]"></i>
                <div class="status-info">
                  <h3 class="status-title">{{ statusTextMap[status] }}</h3>
                  <p class="status-count">{{ count }}</p>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 主要数据展示区 -->
        <el-row :gutter="20" class="data-section">
          <!-- 最近发布 -->
          <el-col :span="12">
            <el-card>
              <div slot="header" class="card-header">
                <span>最近发布</span>
                <el-button
                    type="text"
                    @click="$router.push('/my-posts')">
                  查看全部 <i class="el-icon-arrow-right"></i>
                </el-button>
              </div>
              <el-table :data="dashboardData.recent_posts">
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

          <!-- 我的收藏 -->
          <el-col :span="12">
            <el-card>
              <div slot="header" class="card-header">
                <span>我的收藏</span>
                <el-button
                    type="text"
                    @click="$router.push('/my-bookmarks')">
                  查看全部 <i class="el-icon-arrow-right"></i>
                </el-button>
              </div>
              <el-table :data="dashboardData.bookmarks">
                <el-table-column
                    prop="title"
                    label="标题"
                    min-width="120">
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
        </el-row>

        <!-- 统计和通知区 -->
        <el-row :gutter="20" class="data-section">
          <!-- 统计图表 -->
          <el-col :span="12">
            <el-card>
              <div slot="header" class="card-header">
                <span>最近7天发布统计</span>
              </div>
              <v-chart
                  class="chart-wrapper"
                  :option="chartOption"
                  autoresize
                  v-if="hasChartData"
              />
              <div v-else class="no-data-tip">
                暂无近期发布数据 📊
              </div>
            </el-card>
          </el-col>

          <!-- 未读通知 -->
          <el-col :span="12">
            <el-card>
              <div slot="header" class="card-header">
                <span>未读通知（{{ dashboardData.unread_notifications }}）</span>
                <el-button
                    type="text"
                    @click="markAllAsRead">
                  全部已读
                </el-button>
              </div>
              <div class="notification-list">
                <div
                    v-for="item in dashboardData.notifications"
                    :key="item.id"
                    class="notification-item">
                  <i :class="['icon', notificationIconMap[item.type]]"></i>
                  <div class="content">
                    <div class="time">{{ formatTime(item.created_at) }}</div>
                    <p class="text">{{ item.content }}</p>
                  </div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <!-- 编辑资料对话框 -->
    <el-dialog
        title="修改个人资料"
        :visible.sync="editDialogVisible"
        width="500px"
        @closed="resetForm">
      <el-form
          :model="profileForm"
          label-width="80px"
          ref="profileForm"
          :rules="formRules">
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="profileForm.real_name"></el-input>
        </el-form-item>
        <el-form-item label="联系方式" prop="phone">
          <el-input v-model="profileForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="用户角色">
          <el-tag type="info">{{ roleMap[userInfo.role] }}</el-tag>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button
            type="primary"
            :loading="submitting"
            @click="submitProfile">
          确认修改
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
// import * as echarts from 'echarts';
// 新增的 Vue-ECharts 相关导入
import {use} from 'echarts/core'
import {CanvasRenderer} from 'echarts/renderers'
import {BarChart} from 'echarts/charts'
import {GridComponent, LegendComponent, TitleComponent, TooltipComponent} from 'echarts/components'
import dayjs from "dayjs";
import {post} from "axios";


use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])
export default {
  data() {
    return {
      // 用户信息相关
      userInfo: {
        real_name: '加载中...',
        role: 'student',
        avatar: require('@/assets/touxiang.jpg'),
        phone: ''
      },

      // 仪表盘数据
      dashboardData: {
        recent_posts: [],
        bookmarks: [],
        status_summary: {},
        notifications: [],
        total_posts: 0,
        total_bookmarks: 0,
        unread_notifications: 0,
        daily_stats: []
      },

      // 图表实例
      chartOption: {
        title: {
          text: '近期发布统计',
          left: 'center',
          show: false // 初始隐藏，等待数据加载
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          containLabel: true,
          left: '3%',
          right: '4%',
          bottom: '15%'
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            rotate: 45,
            formatter: (value) => this.formatDate(value)
          }
        },
        yAxis: {
          type: 'value',
          name: '发布数量'
        },
        series: [{
          type: 'bar',
          itemStyle: {color: '#409EFF'}
        }]
      },
      // 编辑对话框状态
      editDialogVisible: false,
      submitting: false,
      profileForm: {
        real_name: '',
        phone: ''
      },

      // 表单验证规则
      formRules: {
        real_name: [
          {required: true, message: '请输入真实姓名', trigger: 'blur'},
          {min: 2, max: 12, message: '长度在2到12个字符', trigger: 'blur'}
        ],
        phone: [
          {pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur'}
        ]
      },

      // 静态配置映射表
      roleMap: {
        student: '学生',
        staff: '教职工',
        admin: '管理员'
      },
      statusTextMap: {
        pending: '待处理',
        active: '进行中',
        completed: '已完成',
        expired: '已过期'
      },
      statusIconMap: {
        pending: 'el-icon-time',
        active: 'el-icon-refresh',
        completed: 'el-icon-circle-check',
        expired: 'el-icon-warning-outline'
      },
      statusTypeMap: {
        pending: 'warning',
        active: 'primary',
        completed: 'success',
        expired: 'danger'
      },
      notificationIconMap: {
        system: 'el-icon-s-comment',
        match: 'el-icon-connection',
        reminder: 'el-icon-alarm-clock'
      },
      requestMethod:'POST'
    }
  },
  computed: {
    uploadAction() {
      return `${this.$http.defaults.baseURL}/user/upload-avatar/`
    },
    uploadHeaders() {
      return {
        'Authorization': `Token ${this.$store.state.token}`,
        'X-CSRFToken': this.getCSRFToken(),
      }
    },
    hasChartData() {
      return this.dashboardData.daily_stats?.length > 0
    },
    chartData() {
      return this.dashboardData.category_stats.map(item => ({
        name: item.name,
        value: item.value
      }))
    },
  },

  methods: {
    post,
    formatTime(time) {
      return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
    },
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
    // 加载数据
    async loadData() {
      try {
        const [userRes, dashboardRes] = await Promise.all([
          this.$http.get('/user/profile/'),
          this.$http.get('/dashboard/')
        ]);
        console.log('API Response Structure:', dashboardRes);
        console.log('User Response:', userRes);
        // 安全解构数据
        // this.userInfo = userRes || {};
        this.userInfo = {
          real_name: userRes.real_name || '',
          role: userRes.role || '',
          phone: userRes.phone || '',
          avatar: userRes.avatar || '',
        }
        console.log('User Avatar URL:', this.userInfo.avatar); // 打印头像 URL

        this.dashboardData = {
          daily_stats: dashboardRes.data.daily_stats || [],
          status_summary: dashboardRes.data.status_summary || [],
          category_stats: dashboardRes.data.category_stats || [],
          activity_dates: dashboardRes.data.activity_dates || [],
          unread_notifications: dashboardRes.data.unread_notifications || 0,
          bookmarks: dashboardRes.data.bookmarks || [],
          recent_posts: dashboardRes.data.recent_posts || [],
          notifications: dashboardRes.data.notifications || [],
          total_bookmarks: dashboardRes.data.total_bookmarks || 0,
          total_posts: dashboardRes.data.total_posts || 0,
        }
        this.updateChart();
      } catch (error) {
        this.$message.error('数据加载失败')
        console.error('加载数据出错:', error)
      }
    },
    // 更新图表数据
    updateChart() {
      if (!this.hasChartData) return
      const dates = this.dashboardData.daily_stats.map(d => d.date)
      const counts = this.dashboardData.daily_stats.map(d => d.count)
      this.chartOption = {
        ...this.chartOption,
        title: {
          ...this.chartOption.title,
          show: true
        },
        xAxis: {
          ...this.chartOption.xAxis,
          data: dates
        },
        series: [{
          ...this.chartOption.series[0],
          data: counts,
          name: '每日发布量'
        }]
      }
    },
    // 头像上传处理
    handleAvatarSuccess(res) {
      console.log('res', res)
      if (res.status === 'success' && res.data?.avatar_url) {
        this.userInfo.avatar = `${res.data.avatar_url}?t=${Date.now()}`
        this.$message.success('头像更新成功')
        // 同步到 Vuex store
        this.$store.commit('updateAvatar', this.userInfo.avatar)
      } else {
        this.$message.error(res.message || '头像更新失败')
      }
    },
    // 头像上传预处理
    beforeAvatarUpload(file) {
      const isImage = ['image/jpeg', 'image/png'].includes(file.type);
      const isLt2M = file.size / 1024 / 1024 < 2;
      if (!isImage) {
        this.$message.error('只能上传 JPG/PNG 格式的图片');
        return false;
      }
      if (!isLt2M) {
        this.$message.error('图片大小不能超过2MB');
        return false;
      }
      return true;
    },
    // 通知相关方法
    markAllAsRead() {
      this.$confirm('确定要标记所有通知为已读吗？', '操作确认', {
        type: 'warning'
      }).then(async () => {
        await this.$http.post('/notifications/mark-all-read/')
        await this.loadData()
        this.$message.success('操作成功')
      }).catch(() => {
      })
    },
    // 用户资料编辑
    showEditDialog() {
      this.profileForm = {...this.userInfo}
      this.editDialogVisible = true
    },
    resetForm() {
      this.$refs.profileForm.resetFields()
    },
    submitProfile() {
      this.$refs.profileForm.validate(async valid => {
        if (!valid) return
        this.submitting = true
        try {
          await this.$http.put('/user/profile/', this.profileForm)
          this.userInfo = {...this.profileForm} //将profileForm对象的所有属性和值复制到userInfo对象中，实现了对象的浅拷贝
          this.$message.success('资料更新成功')
          this.editDialogVisible = false
        } catch (error) {
          console.error('更新失败:', error)
        } finally {
          this.submitting = false
        }
      })
    },
    // 时间格式化
    formatDate(dateStr) {
      return dateStr.slice(5) // 显示月-日(例如 03-13)
    },
    getCSRFToken() {
      const cookieValue = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1] || '';
      return cookieValue;
    }
  },
  mounted() {
    this.loadData();
  },
}

</script>

<style lang="scss" scoped>
// 颜色变量
$primary-color: #409EFF;
$success-color: #67C23A;
$warning-color: #E6A23C;
$danger-color: #F56C6C;
$text-primary: #303133;
$text-regular: #606266;
$text-secondary: #909399;
$border-color: #DCDFE6;
$bg-color: #f5f7fa;
$card-bg: #ffffff;

.dashboard-container {
  padding: 24px;
  background: $bg-color;
  min-height: calc(100vh - 84px);
}

/* 卡片全局样式 */
.el-card {
  margin-bottom: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-2px);
  }

  ::v-deep .el-card__header {
    padding: 18px 24px;
    border-bottom: 1px solid rgba($border-color, 0.6);
    background: linear-gradient(135deg, rgba($primary-color, 0.05), transparent);
  }

  ::v-deep .el-card__body {
    padding: 24px;
  }
}

/* 用户信息区域 */
.user-card {
  .user-info {
    text-align: center;

    // 头像上传
    .avatar-uploader {
      width: 128px;
      height: 128px;
      margin: 0 auto 20px;
      border: 2px dashed rgba($primary-color, 0.3);
      border-radius: 50%;
      overflow: hidden;
      cursor: pointer;
      transition: border-color 0.3s;

      &:hover {
        border-color: $primary-color;
        .avatar-uploader-icon {
          color: $primary-color;
        }
      }

      .avatar {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .avatar-uploader-icon {
        color: $text-secondary;
        font-size: 32px;
        line-height: 128px;
        transition: color 0.3s;
      }
    }

    // 用户名称
    .user-name {
      margin: 0 0 8px;
      font-size: 20px;
      font-weight: 600;
      color: $text-primary;
    }

    // 用户角色
    .user-role {
      margin: 0 0 24px;
      color: $text-secondary;
      font-size: 14px;
      letter-spacing: 0.5px;
    }
  }

  // 统计信息
  .stats-wrapper {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0;

    .stat-item {
      padding: 12px;
      background: rgba($primary-color, 0.08);
      border-radius: 8px;
      text-align: center;

      .stat-number {
        display: block;
        font-size: 22px;
        font-weight: 600;
        color: $primary-color;
        line-height: 1.2;
      }

      .stat-label {
        font-size: 12px;
        color: $text-secondary;
        letter-spacing: 0.3px;
      }
    }
  }

  // 操作按钮组
  .el-button {
    margin-top: 16px;
    width: 100%;
  }
}

/* 快捷操作区域 */
.quick-actions {
  .el-button {
    margin-bottom: 12px;
    width: 100%;
    transition: all 0.3s;

    &:last-child {
      margin: 0;
    }

    &:hover {
      transform: translateY(-6px);
    }
  }
}

/* 状态统计卡片 */
.status-card {
  .status-content {
    display: flex;
    align-items: center;
    padding: 8px;

    .status-icon {
      width: 48px;
      height: 48px;
      font-size: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 8px;
      background: rgba($primary-color, 0.1);
      color: $primary-color;
      flex-shrink: 0;
    }

    .status-info {
      margin-left: 16px;

      .status-title {
        margin: 0;
        font-size: 14px;
        color: $text-secondary;
      }

      .status-count {
        margin: 4px 0 0;
        font-size: 24px;
        font-weight: 600;
        color: $text-primary;
      }
    }
  }
}

/* 表格区域 */
.data-section {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 500;

    .el-button {
      padding: 4px 8px;
    }
  }

  .el-table {
    border-radius: 8px;

    ::v-deep th.el-table__cell {
      background: rgba($primary-color, 0.06) !important;
    }

    ::v-deep .el-tag {
      border-radius: 4px;
      font-weight: 500;
    }
  }
}

/* 图表区域 */
.chart-wrapper {
  height: 320px;
}

.no-data-tip {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: $text-secondary;
  flex-direction: column;

  &::before {
    content: "📊";
    font-size: 48px;
    margin-bottom: 12px;
  }
}

/* 通知列表 */
.notification-list {
  .notification-item {
    display: flex;
    padding: 16px 0;
    border-bottom: 1px solid rgba($border-color, 0.4);

    &:last-child {
      border-bottom: none;
    }

    .icon {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      background: rgba($primary-color, 0.1);
      color: $primary-color;
      font-size: 18px;
      flex-shrink: 0;
    }

    .content {
      margin-left: 16px;

      .time {
        font-size: 12px;
        color: $text-secondary;
        margin-bottom: 4px;
      }

      .text {
        margin: 0;
        font-size: 14px;
        color: $text-primary;
        line-height: 1.4;
      }
    }
  }
}

/* 响应式适配 */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }

  .stats-wrapper {
    grid-template-columns: 1fr !important;
  }

  .el-col-md-8 {
    margin-bottom: 16px;
  }

  .data-section .el-col {
    margin-bottom: 16px;
  }
}
</style>

