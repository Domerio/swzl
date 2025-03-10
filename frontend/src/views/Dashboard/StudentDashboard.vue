<template>
  <div class="student-dashboard">
    <el-container>
      <el-header class="dashboard-header">
        <div class="header-left">
          <h2 class="title">校园失物招领平台</h2>
          <span class="welcome">欢迎回来，{{ user.real_name }}同学</span>
        </div>
        <div class="header-right">
          <el-badge :value="unreadMessages" class="message-badge">
            <el-button icon="el-icon-bell" circle @click="showMessages"></el-button>
          </el-badge>
          <el-button type="danger" plain @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>

      <el-main>
        <!-- 数据概览卡片 -->
        <el-row :gutter="20" class="mb-20">
          <el-col :span="6" v-for="(stat, index) in statsData" :key="index">
            <stat-card
                :title="stat.title"
                :value="stat.value"
                :icon="stat.icon"
                :color="stat.color"
            />
          </el-col>
        </el-row>

        <!-- 主要功能区域 -->
        <el-row :gutter="20">
          <!-- 个人信息及快捷操作 -->
          <el-col :span="6">
            <user-profile :user="user" class="mb-20"/>
            <quick-actions @lost="handleLostItem" @found="handleFoundItem"/>
          </el-col>

          <!-- 通知公告 -->
          <el-col :span="18">
            <el-card class="feature-card">
              <template #header>
                <div class="card-header">
                  <span>最新动态</span>
                  <el-button type="text" @click="viewAllRecords">查看全部 ></el-button>
                </div>
              </template>
              <record-table :data="recentRecords"/>
            </el-card>

            <!-- 数据可视化 -->
            <el-card class="feature-card mt-20">
              <template #header>
                <span>失物分布分析</span>
              </template>
              <div ref="chart" style="height: 300px;"></div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </el-container>

    <!-- 消息弹窗 -->
    <message-dialog v-model="showMessageDialog"/>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
// import * as echarts from 'echarts'
import StatCard from '../../components/StatCard.vue'
import UserProfile from '../../components/UserProfile.vue'
import QuickActions from '../../components/QuickActions.vue'
import RecordTable from '../../components/RecordTable.vue'
import MessageDialog from '../../components/MessageDialog.vue'

export default {
  name: 'StudentDashboard',
  components: {
    StatCard,
    UserProfile,
    QuickActions,
    RecordTable,
    MessageDialog
  },
  data() {
    return {
      statsData: [
        {title: '我的发布', value: 0, icon: 'el-icon-document', color: '#409EFF'},
        {title: '正在跟进', value: 0, icon: 'el-icon-s-order', color: '#67C23A'},
        {title: '已解决问题', value: 0, icon: 'el-icon-success', color: '#E6A23C'},
        {title: '未读消息', value: 0, icon: 'el-icon-message', color: '#F56C6C'}
      ],
      recentRecords: [],
      showMessageDialog: false,
      unreadMessages: 0,
      chartInstance: null
    }
  },
  computed: {
    ...mapGetters(['currentUser']),
    user() {
      return this.currentUser || {}
    }
  },
  mounted() {
    // this.initChart()
    // this.fetchData()
  },
  methods: {
    mockChartData() {
      return [
        {name: '教学楼', value: 40},
        {name: '食堂', value: 25},
        {name: '图书馆', value: 20},
        {name: '体育场', value: 15}
      ]
    }
  },
  async fetchData() {
    if (process.env.NODE_ENV === 'development') {
      this.mockChartData()
      return
    }
    try {
      // 1. 获取统计信息
      const {data: stats} = await this.$http.get('/api/dashboard/stats/')
      this.statsData = this.statsData.map(item => ({
        ...item,
        value: stats[item.key] || 0
      }))

      // 2. 获取最近记录
      const {data: records} = await this.$http.get('/api/records/recent/')
      this.recentRecords = records.map(item => ({
        id: item.id,
        title: item.title,
        type: item.item_type === 'lost' ? '丢失物品' : '捡到物品',
        status: item.status,
        date: this.$dayjs(item.created_at).format('YYYY-MM-DD')
      }))
      // 3. 更新图表数据
      const {data: chartData} = await this.$http.get('/api/chart/category-stats/')
      this.updateChart(chartData)
      // 4. 获取未读消息数量（已包含在statsData里）
      this.unreadMessages = stats.unread_messages
    } catch (error) {
      this.handleFetchError(error)
    }
  },

  updateChart(data) {
    const option = {
      tooltip: {
        formatter: '{b}: {c} ({d}%)'
      },
      series: [{
        data: data.map(item => ({
          value: item.count,
          name: item.name,
          itemStyle: {
            color: this.generateChartColor(item.name)
          }
        }))
      }]
    }
    this.chartInstance.setOption(option)
  },
  handleFetchError(error) {
    if (error.response?.status === 401) {
      this.$message.error('登录已过期，请重新登录')
      this.$store.dispatch('logout')
      this.$router.push('/login')
    } else {
      this.$message.error('数据加载失败')
    }
  },

  handleLogout() {
    this.$confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    }).then(() => {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    })
  },

  handleLostItem() {
    this.$router.push('/report-lost')
  },

  handleFoundItem() {
    this.$router.push('/report-found')
  },

  showMessages() {
    this.showMessageDialog = true
  },

  viewAllRecords() {
    this.$router.push('/my-records')
  },
  generateChartColor() {
    const colors = ['#5470C6', '#91CC75', '#EE6666', '#73C0DE', '#3BA272', '#FC8452', '#9A60B4', '#EA7CC3']
    return colors[Math.floor(Math.random() * colors.length)]
  },
}
</script>

<style scoped lang="scss">
.student-dashboard {
  height: 100vh;
  background: #f5f7fa;

  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #fff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, .1);
    padding: 0 30px;

    .header-left {
      .title {
        font-size: 24px;
        color: #303133;
        margin: 0;
      }

      .welcome {
        color: #909399;
        font-size: 14px;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 20px;

      .message-badge {
        ::v-deep .el-badge__content {
          top: 12px;
          right: 12px;
        }
      }
    }
  }

  .feature-card {
    margin-bottom: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, .1);

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;
    }
  }

  .mb-20 {
    margin-bottom: 20px;
  }

  .mt-20 {
    margin-top: 20px;
  }
}
</style>
