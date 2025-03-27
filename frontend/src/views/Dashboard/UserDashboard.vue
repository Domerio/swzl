<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- 个人信息列 -->
      <el-col :span="6">
        <el-card class="user-card">
          <div class="user-info">
            <el-upload class="avatar-uploader" :action="uploadAction" :headers="uploadHeaders" :show-file-list="false"
              :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload" :method="requestMethod" name="file">
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

            <el-button type="primary" size="small" icon="el-icon-edit" @click="showEditDialog">
              修改资料
            </el-button>
          </div>
          <!-- 在用户信息卡片中添加 -->
          <el-button type="danger" size="small" icon="el-icon-switch-button" @click="handleLogout"
            style="margin-top: 15px;">
            安全退出
          </el-button>
        </el-card>

        <!-- 快捷操作区 -->
        <el-card class="quick-actions">
          <div slot="header" class="clearfix">
            <span>快捷功能</span>
          </div>
          <el-button type="primary" icon="el-icon-s-release" @click="handleLostItemRegister">
            失物登记
          </el-button>
          <!-- 添加失物大厅按钮 -->
          <el-button type="info" icon="el-icon-s-shop" @click="goToLostHall">
            失物大厅
          </el-button>
          <el-button type="success" icon="el-icon-s-claim" @click="handleFoundItemRegister">
            招领登记
          </el-button>
          <!-- 添加招领大厅按钮 -->
          <el-button type="warning" icon="el-icon-s-shop" @click="goToFoundHall">
            招领大厅
          </el-button>
        </el-card>
      </el-col>

      <!-- 主要内容区 -->
      <el-col :span="18">
        <!-- 上半部分：最近发布和我的收藏 -->
        <el-row :gutter="20" class="top-section">
          <!-- 最近发布 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12" class="card-wrapper">
            <el-card class="recent-posts">
              <div slot="header" class="card-header">
                <span>最近发布</span>
                <el-button type="text" class="header-action-btn">
                  <i class="el-icon-arrow-right"></i>
                </el-button>
              </div>

              <el-table :data="dashboardData.recent_posts" @row-click="handleRowClick" class="click-table">
                <el-table-column prop="title" label="标题" min-width="120">
                </el-table-column>
                <el-table-column label="类型" width="100">
                  <template slot-scope="scope">
                    {{ getItemTypeLabel(scope.row.item_type) }}
                  </template>
                </el-table-column>

                <el-table-column prop="category" label="分类" width="100">
                </el-table-column>
                <el-table-column label="状态" width="100">
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
          <el-col :xs="24" :sm="24" :md="12" :lg="12" class="card-wrapper">
            <el-card class="my-collection">
              <div slot="header" class="card-header">
                <span>我的收藏</span>
                <el-button type="text" class="header-action-btn" @click="$router.push('/my-bookmarks')">
                  查看全部 <i class="el-icon-arrow-right"></i>
                </el-button>
              </div>
              <el-table :data="dashboardData.bookmarks" @row-click="handleRowClick" class="clickable-table">
                <el-table-column prop="title" label="标题" min-width="120">
                </el-table-column>
                <el-table-column label="类型" width="100">
                  <template slot-scope="scope">
                    {{ getItemTypeLabel(scope.row.item_type) }}
                  </template>
                </el-table-column>

                <el-table-column label="状态" width="100">
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

        <!-- 下半部分：统计图表和通知区 -->
        <el-row :gutter="20" class="bottom-section">
          <!-- 统计图表 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12" class="chart-col">
            <el-card class="stats-card">
              <div slot="header" class="card-header">
                <span>最近7天发布统计</span>
                <el-button type="text" class="header-action-btn">
                </el-button>
              </div>
              <div ref="chart" class="chart-wrapper" v-show="hasChartData"></div>
              <div v-if="!hasChartData" class="no-data-tip">
                暂无近期发布数据 📊
              </div>
            </el-card>
          </el-col>

          <!-- 未读通知 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12" class="notification-col">
            <el-card class="notification-card">
              <div slot="header" class="card-header">
                <span>未读通知（{{ dashboardData.unread_notifications }}）</span>
                <el-button type="text" class="header-action-btn" @click="markAllAsRead">
                  全部已读
                </el-button>
              </div>

              <div class="notification-list">
                <div v-for="item in dashboardData.notifications" :key="item.id" class="notification-item"
                  @click="handleNotificationClick(item)">
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
    <el-dialog title="修改个人资料" :visible.sync="editDialogVisible" width="500px" @closed="resetForm">
      <el-form :model="profileForm" label-width="80px" ref="profileForm" :rules="formRules">
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
        <el-button type="primary" :loading="submitting" @click="submitProfile">
          确认修改
        </el-button>
      </div>
    </el-dialog>
    <!-- 失物详情弹窗 -->
    <el-dialog title="🔍 物品详情" :visible.sync="detailDialogVisible" width="800px" custom-class="item-detail-dialog">
      <el-row :gutter="20">
        <!-- 图片轮播区 -->
        <el-col :span="8">
          <el-carousel :interval="5000" height="300px" arrow="always">
            <el-carousel-item v-for="(img, index) in currentItem.images" :key="index">
              <el-image :src="img" fit="cover" class="detail-image">
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
            </el-carousel-item>
          </el-carousel>
        </el-col>
        <!-- 详细信息区 -->
        <el-col :span="16">
          <el-descriptions :column="2" border label-class-name="detail-label">
            <el-descriptions-item label="物品名称">{{ currentItem.title }}</el-descriptions-item>
            <el-descriptions-item label="物品分类">
              {{ currentItem.category_name }}
            </el-descriptions-item>
            <el-descriptions-item label="丢失时间">
              {{ formatTime(currentItem.lost_time) }}
            </el-descriptions-item>
            <!--            <el-descriptions-item label="丢失地点">{{ currentItem.location }}</el-descriptions-item>-->
            <el-descriptions-item label="丢失地点">
              {{ currentItem.location }}
              <!-- 添加地图容器 -->
              <div v-if="currentItem.location_lat && currentItem.location_lng" class="detail-map-container"
                :id="'detail-map-' + currentItem.id"></div>
            </el-descriptions-item>
            <el-descriptions-item label="发布类型">
              {{ currentItem.item_type === 'lost' ? '失物登记' : '招领登记' }}
            </el-descriptions-item>

            <el-descriptions-item label="当前状态">
              <el-tag :type="statusTypeMap[currentItem.status]" size="medium">
                {{ statusTextMap[currentItem.status] }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="登记时间">
              {{ formatTime(currentItem.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="联系方式" :span="2">
              <el-link type="primary" :href="currentItem.contact">
                {{ currentItem.contact }}
              </el-link>
            </el-descriptions-item>
            <el-descriptions-item label="详细描述" :span="2">
              <pre class="description-pre">{{ currentItem.description }}</pre>
            </el-descriptions-item>
          </el-descriptions>
        </el-col>
      </el-row>
      <!-- 底部操作按钮 -->
      <div slot="footer">
        <el-button @click="detailDialogVisible = false" size="medium">
          关闭
        </el-button>
        <el-button type="warning" v-if="currentItem.status === 'pending' && currentItem.user === userInfo.id"
          @click="showEditItemDialog" size="medium">
          修改物品
        </el-button>
        <el-button type="danger"
          v-if="currentItem.status === 'active' && currentItem.item_type === 'lost' && currentItem.user === userInfo.id"
          @click="handleCloseItem" size="medium">
          标记为已找回
        </el-button>
        <!-- 添加删除按钮 -->
        <el-button type="danger" @click="handleDeleteItem" size="medium">
          删除物品
        </el-button>
      </div>
    </el-dialog>
    <!-- 物品编辑对话框 -->
    <el-dialog title="修改物品信息" :visible.sync="editItemDialogVisible" width="600px">
      <el-form :model="editItemForm" label-width="80px">
        <el-form-item label="物品名称">
          <el-input v-model="editItemForm.title"></el-input>
        </el-form-item>
        <el-form-item label="物品分类">
          <el-select v-model="editItemForm.category" placeholder="请选择分类">
            <el-option v-for="item in categories" :key="item.value" :label="item.label" :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="详细描述">
          <el-input type="textarea" :rows="4" v-model="editItemForm.description">
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="editItemDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitItemEdit">确认修改</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import dayjs from "dayjs";
import axios, { post } from "axios";
import * as echarts from 'echarts';


export default {
  /* eslint-disable no-undef */
  data() {
    return {
      // 用户信息相关
      userInfo: {
        real_name: '加载中...',
        role: '',
        avatar: require('@/assets/touxiang.jpg'),
        phone: '',
        id: ''
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
          itemStyle: { color: '#409EFF' }
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
          { required: true, message: '请输入真实姓名', trigger: 'blur' },
          { min: 2, max: 12, message: '长度在2到12个字符', trigger: 'blur' }
        ],
        phone: [
          { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' }
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
      requestMethod: 'POST',
      detailDialogVisible: false,
      currentItem: {}, // 当前查看的条目
      chart: null,
      editItemDialogVisible: false,
      editItemForm: {},
      categories: [], // 存放分类数据
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
    // 显示编辑对话框
    showEditItemDialog() {
      this.editItemForm = { ...this.currentItem };
      this.loadCategories();
      this.editItemDialogVisible = true;
    },
    // 加载分类数据
    async loadCategories() {
      try {
        let response = null;
        if (this.currentItem.item_type === 'lost') {
          response = await this.$http.get('/lost/categories/');
        } else if (this.currentItem.item_type === 'found') {
          response = await this.$http.get('/found/categories/')
        }
        this.categories = response.map(item => ({
          value: item.id,
          label: item.name
        }));
      } catch (error) {
        console.error('加载分类失败:', error);
      }
    },

    // 提交修改
    async submitItemEdit() {
      try {
        const response = await this.$http.put(
          `/user/items/${this.editItemForm.id}/`,
          this.editItemForm
        );

        // 更新当前展示的条目
        this.currentItem = {
          ...this.currentItem,
          ...response.data,
          // category_name: this.categories.find(c => c.value === response.data.category)?.label
        };
        console.log(response);
        
        this.$message.success('修改成功');
        this.editItemDialogVisible = false;
        // 更新当前条目显示
        this.currentItem = {
          ...this.currentItem,
          ...response.data,
          category_name: response.category_name
        };
        // 更新最近发布列表
        const index = this.dashboardData.recent_posts.findIndex(
          item => item.id === this.currentItem.id
        );
        if (index > -1) {
          this.dashboardData.recent_posts.splice(index, 1, {
            ...this.currentItem,
            category: response.category_name
          });
        }
      } catch (error) {
        this.$message.error('修改失败: ' + (error.response?.data?.detail || error.message));
      }
    },
    // 处理单个通知点击
    async handleNotificationClick(notification) {
      try {
        if (!notification?.id) {
          throw new Error('无效的通知ID')
        }
        // 标记为已读
        await this.$http.patch(`/notifications/${notification.id}/`,
          {
            is_read: true
          }
        );
        console.log('notification:', notification);
        // 如果有相关物品则跳转
        if (notification.related_item_id) {
          // this.$router.push(`/items/${notification.related_item_id}`);
          this.handleItemDetail(notification.related_item_id)
        }
        // 移除已读通知
        this.dashboardData.notifications = this.dashboardData.notifications.filter(
          n => n.id !== notification.id
        );

        // 更新未读计数
        this.dashboardData.unread_notifications -= 1;

      } catch (error) {
        console.error('通知处理失败:', error.response || error); // 添加详细日志
        this.$message.error(`处理失败: ${error.response?.data?.error || error.message}`);
      }
    },
    // 处理删除物品的方法
    handleDeleteItem() {
      // 确认用户是否真的要删除物品
      this.$confirm('确定要删除该物品吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 发送删除请求
        axios.delete(`/api/user/items/${this.currentItem.id}/delete/`)
          .then(() => {
            // 删除成功后，更新页面数据
            this.dashboardData.recent_posts = this.dashboardData.recent_posts.filter(item => item.id !== this.currentItem.id);
            this.detailDialogVisible = false;
            this.$message.success('物品删除成功');
          })
          .catch(error => {
            this.$message.error('物品删除失败：' + error.message);
          });
      }).catch(() => {
        // 用户取消删除操作
        this.$message.info('删除操作已取消');
      });
    },
    getItemTypeLabel(type) {
      return type === 'lost' ? '失物登记' : '招领登记';
    },

    getCategoryName(categoryId) {
      return axios.get(`/api/category/name/${categoryId}/`)
        .then(response => response.data.name)
        .catch(() => '未知分类');
    },
    // 点击表格行触发
    async handleRowClick(row) {
      const apiUrl = `/items/${row.id}/`;
      console.log('Request URL:', apiUrl); // 打印请求地址
      try {
        const response = await this.$http.get(apiUrl);
        console.log('get response:', response);
        // 新增：获取分类名称并合并到数据
        const categoryName = await this.getCategoryName(response.category);
        this.currentItem = {
          ...response,
          category_name: categoryName,
          images: response.images || []  // 确保有图册数据
        };
        this.detailDialogVisible = true;
      } catch (error) {
        this.$message.error('获取详情失败');
      }
    },
    async handleItemDetail(itemId) {
      const apiUrl = `/items/${itemId}/`;
      console.log('Request URL:', apiUrl); // 打印请求地址
      try {
        const response = await this.$http.get(apiUrl);
        console.log('get response:', response);
        // 新增：获取分类名称并合并到数据
        const categoryName = await this.getCategoryName(response.category);
        this.currentItem = {
          ...response,
          category_name: categoryName,
          images: response.images || []  // 确保有图册数据
        };
        this.detailDialogVisible = true;
      } catch (error) {
        this.$message.error('获取详情失败');
      }
    },
    // 标记为已找回
    async handleCloseItem() {
      try {
        console.log(this.currentItem.id)
        const response = await this.$http.patch(
          `/user/items/${this.currentItem.id}/status/`,
          { status: 'completed' },  // 只传必要参数
          {
            headers: {
              'X-Requested-With': 'XMLHttpRequest',
              'Content-Type': 'application/json'
            }
          }
        )
        console.log("状态更新响应:", response.data)
        this.$message.success('操作成功')

        // 刷新数据时强制从服务器获取
        await this.loadData(true)
        this.detailDialogVisible = false

      } catch (error) {
        console.error("标记已找回失败:", {
          error: error.response?.data || error.message,
          config: error.config
        })
        this.$message.error(`操作失败: ${error.response?.data?.error || '服务器错误'}`)
      }
    },

    // 处理上传成功
    post,
    formatTime(time) {
      return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
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
    // 加载数据
    async loadData() {
      try {
        const [userRes, dashboardRes] = await Promise.all([
          this.$http.get('/user/profile/'),
          this.$http.get('/dashboard/')
        ]);
        this.userInfo = {
          real_name: userRes.real_name || '',
          role: userRes.role || '',
          phone: userRes.phone || '',
          avatar: userRes.avatar || '',
          id: userRes.id || ''
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
      if (this.chart) {
        this.chart.setOption(this.chartOption, true) // 更新图表
        this.chart.resize() // 重新调整图表大小
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
    async markAllAsRead() {
      try {
        await this.$http.post('/notifications/mark-all-read/');
        // 清空通知列表并重置计数
        this.dashboardData.notifications = [];
        this.dashboardData.unread_notifications = 0;
        this.$message.success('全部标记已读成功');
      } catch (error) {
        this.$message.error('操作失败');
      }
    },
    // 用户资料编辑
    showEditDialog() {
      this.profileForm = { ...this.userInfo }
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
          this.userInfo = { ...this.profileForm } //将profileForm对象的所有属性和值复制到userInfo对象中，实现了对象的浅拷贝
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
    },
    handleLostItemRegister() {
      this.$router.push('/api/items/lost/')
    },
    handleFoundItemRegister() {
      this.$router.push('/api/items/found/')
    },
    goToLostHall() {
      this.$router.push('/api/user/lost-hall/')
    },
    goToFoundHall() {
      this.$router.push('/api/user/found-hall/')
    },
    // 初始化详情地图
    initDetailMap() {
      if (!window.AMap) {
        this.$message.warning('地图资源正在加载，请稍候')
        return
      }
      const lng = parseFloat(this.currentItem.location_lng)
      const lat = parseFloat(this.currentItem.location_lat)
      if (isNaN(lng) || isNaN(lat)) return

      this.destroyDetailMap()

      const mapContainerId = `detail-map-${this.currentItem.id}`
      const mapContainer = document.getElementById(mapContainerId)
      if (!mapContainer) return

      this.detailMap = new AMap.Map(mapContainerId, {
        zoom: 17,
        center: [lng, lat],
        resizeEnable: true
      })

      // 实例化独立控件
      const scale = new AMap.Scale()
      const toolBar = new AMap.ToolBar({
        position: { bottom: '20px', right: '20px' }
      })

      // 逐个添加控件
      scale.addTo(this.detailMap)
      toolBar.addTo(this.detailMap)

      // 添加标记
      new AMap.Marker({
        position: [lng, lat],
        content: '<div class="location-pin">📍</div>',
        map: this.detailMap
      })
    },

    destroyDetailMap() {
      if (this.detailMap) {
        try {
          this.detailMap.destroy()
        } catch (e) {
          console.warn('地图销毁过程中出现警告:', e.message)
        }
        this.detailMap = null
      }
    },

    // 初始化图表
    initChart() {
      if (!this.$refs.chart) return;
      // 先销毁旧实例
      if (this.chart) {
        this.chart.dispose();
        this.chart = null;
      }
      // 使用nextTick替代setTimeout
      this.$nextTick(() => {
        if (!this.$refs.chart) return;
        try {
          this.chart = echarts.init(this.$refs.chart);
          this.chart.setOption(this.chartOption);
          this.chart.resize();

          // 添加容错的事件监听
          window.addEventListener('resize', this.handleChartResize);
        } catch (error) {
          console.error('图表初始化失败:', error);
        }
      });
    },

    handleChartResize() {
      if (this.chart) {
        this.chart.resize();
      }
    },
  },
  async mounted() {
    await this.loadData()
    this.initChart()
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

    document.addEventListener('keydown', (e) => {
      if (this.detailDialogVisible) {
        if (e.key === 'ArrowLeft') {
          // 切换至上一个对象
        }
        if (e.key === 'ArrowRight') {
          // 切换至下一个对象
        }
      }
    })

  },
  // 添加watch监听对话框状态
  watch: {
    detailDialogVisible(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          if (this.currentItem.location_lat && this.currentItem.location_lng) {
            this.initDetailMap();
          }
        });
      } else {
        this.destroyDetailMap();
      }
    },
  }
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

// 调整卡片高度和间距
.top-section {
  margin-bottom: 20px;

  .card-wrapper {
    margin-bottom: 0;

    .el-card {
      height: 300px;
      display: flex;
      flex-direction: column;

      ::v-deep .el-card__body {
        flex: 1;
        overflow: auto;
      }
    }
  }
}

.bottom-section {
  .chart-col {
    .stats-card {
      height: 360px;

      .chart-wrapper {
        height: 280px; // 增加可视区域
        width: 100%;
        padding-bottom: 12px;
      }
    }
  }

  .notification-col {
    .notification-card {
      height: 360px;

      .notification-list {
        height: calc(280px - 57px);
        overflow-y: auto;
      }
    }
  }
}

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
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;

  .el-button {
    width: calc(50% - 6px);
    /* 保留间距 */
    margin: 0 0 12px 0 !important;
    /* 清除默认边距 */

    &:nth-child(odd) {
      /* 奇数按钮添加右边距 */
      margin-right: 12px !important;
    }

    &:hover {
      transform: translateY(-6px);
    }
  }
}

// 统一卡片头部按钮样式
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 8px !important;

  .header-action-btn {
    padding: 0;
    color: $text-regular;
    transition: all 0.3s;

    &:hover {
      color: $primary-color;
      transform: translateX(4px);

      .el-icon-arrow-right {
        opacity: 1;
        margin-left: 4px;
      }
    }

    .el-icon-arrow-right {
      opacity: 0;
      margin-left: 0;
      transition: all 0.3s;
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

// 详情弹窗样式
.item-detail-dialog {
  .el-dialog__header {
    padding: 20px;
    border-bottom: 1px solid #EBEEF5;

    .el-dialog__title {
      font-size: 20px;
      color: #303133;
    }
  }

  .el-carousel {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

    &__item {
      display: flex;
      align-items: center;
      justify-content: center;
      background: #f8f9fa;
    }
  }

  .detail-label {
    width: 100px;
    font-weight: 500;
    color: #909399;

    &::after {
      content: "：";
    }
  }

  .description-pre {
    white-space: pre-wrap;
    line-height: 1.6;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 4px;
  }
}

// 可点击表格行样式
.clickable-table {
  ::v-deep .el-table__row {
    cursor: pointer;
    transition: background 0.3s;

    &:hover {
      background: rgba(64, 158, 255, 0.08);
    }

    &:active {
      transform: scale(0.98);
    }
  }
}

// 错误图片占位样式
.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #DCDFE6;

  i {
    font-size: 40px;
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
