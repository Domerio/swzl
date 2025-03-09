<template>
  <div class="login-container">
    <el-card class="login-card">
      <div class="title">校园失物招领系统</div>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form ref="loginForm" :model="loginForm" :rules="loginRules">
            <el-form-item prop="username">
              <el-input
                  v-model="loginForm.username"
                  placeholder="学号/工号">
                <i slot="prefix" class="el-input__icon el-icon-user"></i>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                  v-model="loginForm.password"
                  type="password"
                  placeholder="密码"
                  show-password>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" style="width: 100%" @click="handleLogin">
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form ref="registerForm" :model="registerForm" :rules="registerRules">
            <el-form-item prop="username">
              <el-input
                  v-model="registerForm.username"
                  placeholder="学号/工号">
                <i slot="prefix" class="el-input__icon el-icon-user"></i>
              </el-input>
            </el-form-item>


            <!-- 定义一个表单项，用于输入姓名 -->
            <el-form-item prop="name">
              <el-input
                  v-model="registerForm.real_name"
                  placeholder="真实姓名">
                <i slot="prefix" class="el-input__icon el-icon-user"></i>
              </el-input>
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                  v-model="registerForm.password"
                  type="password"
                  placeholder="密码"
                  show-password>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>

            <el-form-item prop="confirmPassword">
              <el-input
                  v-model="registerForm.confirmPassword"
                  type="password"
                  placeholder="确认密码"
                  show-password>
                <i slot="prefix" class="el-input__icon el-icon-lock"></i>
              </el-input>
            </el-form-item>

            <el-form-item prop="role">
              <el-select v-model="registerForm.role" placeholder="请选择身份" style="width: 100%">
                <el-option label="学生" value="student"/>
                <el-option label="教职工" value="staff"/>
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" style="width: 100%" @click="handleRegister">
                注册
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'UserLogin', // 组件名称
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
            name: response.real_name || response.name
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
        this.$message.success(response.message || '注册成功')// 等待 Vuex 状态更新完成
        await this.$nextTick();
        // 注册成功后自动登录
        await this.$store.dispatch('login', {
          token: response.token,
          user: {
            id: response.user_id,
            username: response.username,
            role: response.role,
            name: response.real_name || response.name
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
        this.$router.replace(roleRouteMap[response.role] || '/').catch(err => {
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

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #8BC6EC 0%, #9599E2 100%);
}

.login-card {
  width: 400px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #409EFF;
}

.el-tabs {
  margin-top: 20px;
}
</style>