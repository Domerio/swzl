<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="brand-section">
        <div class="logo"></div>
        <h1 class="title">校园失物招领系统</h1>
        <p class="subtitle">LOST & FOUND MANAGEMENT SYSTEM</p>
      </div>
      <el-tabs
          v-model="activeTab"
          class="auth-tabs">
        <!--        @tab-click="handleTabClick"-->

        <!-- 登录 Tab -->
        <el-tab-pane label="登录" name="login">
          <transition name="fade-slide" mode="out-in">
            <el-form
                ref="loginForm"
                :model="loginForm"
                :rules="loginRules"
                class="auth-form"
                label-position="top"
            >
              <el-form-item prop="username">
                <el-input
                    v-model="loginForm.username"
                    placeholder="学号/工号"
                    prefix-icon="el-icon-user"
                    size="medium"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input
                    v-model="loginForm.password"
                    type="password"
                    placeholder="密码"
                    show-password
                    prefix-icon="el-icon-lock"
                    size="medium"
                />
              </el-form-item>
              <el-button
                  type="primary"
                  class="submit-btn"
                  size="medium"
                  @click="handleLogin"
              >
                立即登录
              </el-button>
            </el-form>
          </transition>
        </el-tab-pane>
        <!-- 注册 Tab -->
        <el-tab-pane label="注册" name="register">
          <transition name="fade-slide" mode="out-in">
            <el-form
                ref="registerForm"
                :model="registerForm"
                :rules="registerRules"
                class="auth-form"
                label-position="top"
            >
              <!-- 账号输入 -->
              <el-form-item prop="username">
                <el-input
                    v-model="registerForm.username"
                    placeholder="学号/工号"
                    prefix-icon="el-icon-user"
                    size="medium"
                />
              </el-form-item>
              <!-- 真实姓名 -->
              <el-form-item prop="name">
                <el-input
                    v-model="registerForm.real_name"
                    placeholder="真实姓名"
                    prefix-icon="el-icon-s-custom"
                    size="medium"
                />
              </el-form-item>
              <!-- 密码 -->
              <el-form-item prop="password">
                <el-input
                    v-model="registerForm.password"
                    type="password"
                    placeholder="密码"
                    show-password
                    prefix-icon="el-icon-lock"
                    size="medium"
                />
              </el-form-item>
              <!-- 确认密码 -->
              <el-form-item prop="confirmPassword">
                <el-input
                    v-model="registerForm.confirmPassword"
                    type="password"
                    placeholder="确认密码"
                    show-password
                    prefix-icon="el-icon-key"
                    size="medium"
                />
              </el-form-item>
              <!-- 身份选择 -->
              <el-form-item prop="role">
                <el-select
                    v-model="registerForm.role"
                    placeholder="请选择身份"
                    class="full-width"
                    size="medium"
                >
                  <el-option
                      label="学生"
                      value="student"
                      class="role-option"
                  />
                  <el-option
                      label="教职工"
                      value="staff"
                      class="role-option"
                  />
                </el-select>
              </el-form-item>
              <el-button
                  type="primary"
                  class="submit-btn"
                  size="medium"
                  @click="handleRegister"
              >
                立即注册
              </el-button>
            </el-form>
          </transition>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>


<script>
export default {
  name: 'AuthPage',
  data() {
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      activeTab: 'login',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        real_name: '',
        password: '',
        confirm_Password: '',
        role: '',
        csrfToken: '',
      },
      loginRules: {
        username: [{required: true, message: '请输入学号/工号', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}]
      },
      registerRules: {
        username: [{required: true, message: '请输入学号/工号', trigger: 'blur'}],
        real_name: [{required: true, message: '请输入姓名', trigger: 'blur'}],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          {min: 6, message: '密码长度不能小于6位', trigger: 'blur'}
        ],
        confirmPassword: [
          {required: true, message: '请确认密码', trigger: 'blur'},
          {validator: validateConfirmPassword, trigger: 'blur'}
        ],
        role: [{required: true, message: '请选择身份', trigger: 'change'}]
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        await this.$refs.loginForm.validate()
        const response = await this.$http({
          url: '/login/',
          method: 'post',
          data: {
            username: this.loginForm.username,
            password: this.loginForm.password
          }
        })

        // 存储token和用户信息
        await this.$store.dispatch('login', {
          token: response.token,
          user: {
            id: response.user_id,
            username: response.username,
            role: response.role,
            real_name: response.real_name
          }
        })

        this.$message.success('登录成功')

        // 根据角色直接跳转到对应页面
        const roleRouteMap = {
          student: '/student-dashboard',
          staff: '/staff-dashboard',
          admin: '/admin-dashboard'
        }

        // 获取重定向地址或使用默认路由
        const redirect = this.$route.query.redirect || roleRouteMap[response.role] || '/'

        // 使用 replace 而不是 push 来避免在历史记录中留下多余的记录
        this.$router.replace(redirect).catch(err => {
          if (err.name !== 'NavigationDuplicated') {
            console.error('Navigation error:', err)
            this.$router.replace(roleRouteMap[response.role] || '/')
          }
        })
      } catch (error) {
        console.error('Login error:', error)
        const errorMsg = error.response?.data?.error || error.response?.data?.message || '登录失败，请检查用户名和密码'
        this.$message.error(errorMsg)
      }
    },

    handleRegister: async function () {
      try {
        // 验证表单
        await this.$refs.registerForm.validate()

        // 先获取CSRF令牌
        const csrfToken = await this.$http.get('/csrf-token/')
        // 打印发送的数据，用于调试
        const data = {
          username: this.registerForm.username,
          password: this.registerForm.password,
          confirm_password: this.registerForm.confirmPassword,
          real_name: this.registerForm.real_name,
          role: this.registerForm.role,
          // csrfToken: this.registerForm.csrfToken
          csrfToken: csrfToken,
        };
        console.log('Sending registration data:', data);
        // 发送注册请求
        const response = await this.$http({
          url: '/register/',
          method: 'post',
          data: data
        })
        // 显示注册成功的消息
        this.$message.success(response.message || '注册成功')
        await this.$nextTick();
        // 注册成功后自动登录
        await this.$store.dispatch('login', {
          token: response.token,
          user: {
            id: response.user_id,
            username: response.username,
            role: response.role,
            real_name: response.real_name
          }
        })
        // 等待 Vuex 状态更新完成
        await this.$nextTick()
        // 根据角色跳转到对应的仪表板
        const roleRouteMap = {
          student: '/student-dashboard',
          staff: '/staff-dashboard',
          admin: '/admin-dashboard'
        }
        // 跳转到对应的仪表板
        await this.$router.replace(roleRouteMap[response.role] || '/')
            .catch(err => {
              if (err.name !== 'NavigationDuplicated') {
                console.error('Navigation error:', err)
              }
            })
        this.$message.success(response.message || '登录成功')
      } catch (error) {
        console.error('Register error:', error)
        if (error.response && error.response.data) {
          const errorData = error.response.data.error
          if (typeof errorData === 'object') {
            // 处理字段级别的错误
            Object.keys(errorData).forEach(field => {
              this.$message.error(`${field}: ${errorData[field]}`)
            })
          } else {
            // 处理一般错误消息
            this.$message.error(errorData || '注册失败，请重试')
          }
        } else {
          this.$message.error('注册失败，请重试')
        }
      }
    }
  }
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 440px;
  min-width: 320px;
  border-radius: 16px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  overflow: visible;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translateY(-3px);
  }
}

.brand-section {
  text-align: center;
  padding: 24px 0 16px;

  .logo {
    width: 72px;
    height: 72px;
    margin: 0 auto 18px;
    background: #409EFF;
    border-radius: 18px;
    position: relative;
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);

    &::after {
      content: 'LF';
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: white;
      font-weight: 800;
      font-size: 26px;
      letter-spacing: 1px;
    }
  }

  .title {
    font-size: 26px;
    color: #2c3e50;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
    font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  }

  .subtitle {
    color: #7f8c8d;
    font-size: 13px;
    letter-spacing: 1.2px;
    font-weight: 500;
  }
}

.auth-tabs {
  padding: 0 32px;

  ::v-deep .el-tabs__header {
    margin: 0 0 20px 0;
  }

  ::v-deep .el-tabs__nav-wrap {
    display: flex;
    justify-content: center;

    &::after {
      height: 1px;
      background-color: #ecf0f1;
    }
  }

  ::v-deep .el-tabs__active-bar {
    height: 2.8px;
    border-radius: 1.5px;
    background-color: #409EFF;
  }

  ::v-deep .el-tabs__nav {
    width: 100%;
    justify-content: space-around;
  }

  ::v-deep .el-tabs__item {
    flex: 1;
    text-align: center;
    font-size: 15px;
    padding: 0 24px;
    height: 46px;
    transition: all 0.25s ease;

    &:hover {
      color: #66b1ff;
      transform: translateY(-1px);
    }

    &.is-active {
      color: #409EFF;
      font-weight: 600;
    }
  }
}

.auth-form {
  .el-form-item {
    margin-bottom: 22px;

    &::v-deep .el-form-item__content {
      line-height: 1;
    }
  }

  .el-input {
    &::v-deep .el-input__inner {
      height: 44px;
      line-height: 44px;
      padding-left: 42px;
      border-radius: 8px;
      transition: border-color 0.2s ease;

      &:focus {
        border-color: #409EFF;
        box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
      }
    }

    &::v-deep .el-input__prefix {
      left: 12px;
      display: flex;
      align-items: center;
      color: #a0abb6;
    }
  }

  .el-select {
    width: 100%;

    &::v-deep .el-input__inner {
      height: 44px;
      line-height: 44px;
      padding-left: 15px;
    }
  }

  .submit-btn {
    width: 100%;
    height: 44px;
    font-size: 15px;
    font-weight: 500;
    letter-spacing: 0.8px;
    margin-top: 16px;
    border-radius: 8px;
    background-color: #409EFF;
    border-color: #409EFF;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);

    &:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
    }

    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 6px rgba(64, 158, 255, 0.2);
    }
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 12px;
    background: linear-gradient(135deg, #f5f7fa 0%, #dde5f0 100%);
  }
  .login-card {
    border-radius: 14px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  }
  .auth-tabs {
    padding: 0 20px;

    ::v-deep .el-tabs__item {
      font-size: 14px;
      padding: 0 18px;
      height: 44px;
    }
  }
  .brand-section {
    .logo {
      width: 64px;
      height: 64px;
    }

    .title {
      font-size: 23px;
    }

    .subtitle {
      font-size: 12px;
    }
  }
  .auth-form {
    .submit-btn {
      height: 42px;
      font-size: 14px;
    }
  }
}
</style>