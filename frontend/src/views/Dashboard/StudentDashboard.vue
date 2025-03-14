<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 个人信息列 -->
      <el-col :span="6">
        <el-card class="user-card">
          <div class="user-info">
            <el-upload
                class="avatar-uploader"
                action="/api/user/upload-avatar/"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload"
                :upload-avatatar="uploadAvatar">
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
      }
    }
  },
  computed: {
    uploadAction() {
      return `${this.$http.defaults.baseURL}/api/user/upload-avatar`
    },
    uploadHeaders() {
      return{
        'Authorization': `Token ${this.$store.state.token}`
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
    }
  },

  methods: {
    getCSRFToken() {
      return document.cookie.split(';')
          .find(row => row.startsWith('csrftoken'))
      ?.split('=')[1] || '';
    },
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
        // this.userInfo = userRes.data || {};
        this.userInfo = {
          real_name: userRes.real_name || '',
          role: userRes.role || '',
          phone: userRes.phone || '',
          avatar: userRes.avatar || '',
        }
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
      if (res.url) {
        this.userInfo.avatar = res.url + `?t=${Date.now()}` // 添加时间戳以强制刷新图片
        this.$message.success('头像更新成功')
        this.$store.dispatch('api/user/upload-avatar', this.userInfo.avatar)
      }
      // this.userInfo.avatar = res.url
    },
    // 头像上传
    uploadAvatar(file) {
      const response = fetch(`http://localhost:8000/api/user/upload-avatar/`, {
        method: 'POST',
        body: file,
      });
      this.handleAvatarSuccess(response);
    },
    // 头像上传预处理
    beforeAvatarUpload(file) {
      const isImage = ['image/jpeg', 'image/png']
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isImage) {
        this.$message.error('只能上传 JPG/PNG 格式的图片')
      }
      if (!isLt2M) {
        this.$message.error('图片大小不能超过2MB')
      }
      if (isImage && isLt2M)
        this.uploadAvatar(file)
      return isImage.includes(file.type) && isLt2M
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
    }
  },
  mounted() {
    this.loadData();
  },
}

</script>

<style scoped>
.no-data-tip {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #909399;
}

.dashboard-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 84px);
}

/* 用户卡片样式 */
.user-card {
  margin-bottom: 20px;
}

.user-info {
  text-align: center;
}

.avatar-uploader {
  width: 120px;
  height: 120px;
  margin: 0 auto 15px;
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
}

.avatar {
  width: 100%;
  height: 100%;
  display: block;
}

.user-name {
  margin: 10px 0;
  font-size: 18px;
  color: #303133;
}

.user-role {
  color: #909399;
  margin-bottom: 15px;
}

.stats-wrapper {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
  display: block;
}

.stat-label {
  color: #909399;
  font-size: 12px;
}

/* 状态卡片 */
.status-card {
  margin-bottom: 20px;
}

.status-content {
  display: flex;
  align-items: center;
}

.status-icon {
  font-size: 32px;
  margin-right: 15px;
}

.status-title {
  margin: 0 0 5px;
  font-size: 14px;
  color: #909399;
}

.status-count {
  font-size: 24px;
  margin: 0;
  color: #303133;
}

/* 通用卡片头部样式 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 图表容器 */
.chart-wrapper {
  height: 300px;
}
</style>
