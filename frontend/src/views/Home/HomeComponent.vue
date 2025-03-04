<template>
  <!-- 带登录状态显示的响应式导航栏 -->
  <div class="home-container">
    <el-container>
      <!-- 顶部导航 -->
      <el-header height="60px" class="header-nav">
        <el-row type="flex" justify="space-between" align="middle">
          <!-- 品牌标识 -->
          <el-col :span="6">
            <router-link to="/" class="brand-logo">
              <img src="../../assets/logo.png" alt="Site Logo" class="logo">
              <span class="site-name">SWZL 管理系统</span>
            </router-link>
          </el-col>

          <!-- 导航菜单 -->
          <el-col :span="12" class="nav-menu">
            <el-menu
              :default-active="activeMenu"
              mode="horizontal"
              active-text-color="#409EFF"
              @select="handleMenuSelect"
            >
              <el-menu-item index="dashboard">控制台</el-menu-item>
              <el-menu-item index="data">数据管理</el-menu-item>
              <el-menu-item index="analysis">统计分析</el-menu-item>
            </el-menu>
          </el-col>

          <!-- 右侧用户信息 -->
          <el-col :span="6" class="user-info">
            <el-dropdown v-if="userInfo" trigger="click" @command="handleUserCommand">
              <div class="user-panel">
                <el-avatar :size="36" :src="userInfo.avatar || defaultAvatar" />
                <span class="username">{{ userInfo.username }}</span>
                <i class="el-icon-arrow-down el-icon--right" />
              </div>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="settings">账户设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>

            <div v-else class="login-register">
              <el-button type="text" @click="goToLogin">登录</el-button>
              <el-divider direction="vertical" />
              <el-button type="text" @click="goToRegister">注册</el-button>
            </div>
          </el-col>
        </el-row>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="main-content">
        <!-- 动态面包屑 -->
        <div class="breadcrumb-container">
          <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item v-for="(item, index) in breadcrumb" :key="index">
              {{ item }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <!-- 路由视图 -->
        <router-view :key="$route.fullPath"/>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  data() {
    return {
      activeMenu: 'dashboard', // 当前激活菜单项
      breadcrumb: [],          // 动态面包屑路径
      defaultAvatar: require('E:/毕业设计/基于Django的校园失物招领管理系统/lost_and_found_system/frontend/src/assets/touxiang.jpg'),
      userInfo: null           // 用户登录信息
    }
  },
  mounted() {
    this.loadUserInfo()
    this.updateBreadcrumb()
  },
  watch: {
    $route() {
      this.updateBreadcrumb()
    }
  },
  methods: {
    // 加载已登录用户信息
    loadUserInfo() {
      const storedUser = localStorage.getItem('userInfo')
      if (storedUser) {
        try {
          this.userInfo = JSON.parse(storedUser)
        } catch (e) {
          localStorage.removeItem('userInfo')
        }
      }
    },

    // 导航菜单选中处理
    handleMenuSelect(index) {
      this.$router.push({ name: index })
    },

    // 用户操作处理
    handleUserCommand(command) {
      switch (command) {
        case 'logout':
          this.handleLogout()
          break
        case 'profile':
          this.$router.push('/profile')
          break
        case 'settings':
          this.$router.push('/settings')
          break
      }
    },

    // 退出登录
    handleLogout() {
      this.$confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('token')
        localStorage.removeItem('userInfo')
        this.userInfo = null
        this.$router.push('/login')
        this.$message.success('已安全退出')
      })
    },

    // 更新面包屑导航
    updateBreadcrumb() {
      const matched = this.$route.matched.filter(r => r.meta?.title)
      this.breadcrumb = matched.map(r => r.meta.title)
    },

    goToLogin() {
      this.$router.push('/login')
    },

    goToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

<style lang="scss" scoped>
.home-container {
  height: 100vh;
  overflow: hidden;

  .header-nav {
    background: #fff;
    border-bottom: 1px solid #e6e6e6;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);

    .brand-logo {
      display: flex;
      align-items: center;
      text-decoration: none;

      .logo {
        height: 40px;
        margin-right: 12px;
      }

      .site-name {
        font-size: 20px;
        color: #409EFF;
        font-weight: 600;
      }
    }

    .user-info {
      text-align: right;

      .user-panel {
        display: flex;
        align-items: center;
        cursor: pointer;
        padding: 0 12px;
        transition: background 0.3s;

        &:hover {
          background: #f5f7fa;
        }

        .username {
          margin: 0 8px;
          color: #606266;
        }
      }

      .login-register {
        .el-button {
          padding: 0 12px;
          color: #666;

          &:hover {
            color: #409EFF;
          }
        }
      }
    }
  }

  .main-content {
    background: #f5f7fa;
    padding: 20px;

    .breadcrumb-container {
      margin-bottom: 20px;
      padding: 12px;
      background: #fff;
      border-radius: 4px;
      box-shadow: 0 2px 4px rgba(0,0,0,.1);
    }
  }
}
</style>
