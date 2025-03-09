<template>
  <div id="back_count">
    <div class="login-cont">
      <h2>校园失物招领管理系统</h2>
      <div>
        <p>用户名（学号/工号）</p>
        <el-input
            v-model="username"
            placeholder="请输入学号/工号"
            clearable
            @keyup.enter.native="handleLogin"
        ></el-input>
        <span v-if="usernameError" style="color: red">{{ usernameError }}</span>
      </div>
      <div>
        <p>密码</p>
        <el-input
            type="password"
            v-model="pwd"
            placeholder="请输入密码"
            show-password
            clearable
            @keyup.enter.native="handleLogin"
        ></el-input>
      </div>

      <el-button
          class="loginBtn"
          type="primary"
          @click="handleLogin"
          :loading="loading"
      >
        {{ loading ? '登录中...' : '登录' }}
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      pwd: '',
      loading: false,
      usernameError: ''
    }
  },
  methods: {
    async handleLogin() {
      // 学号/工号格式验证
      if (!/^\d{8,12}$/.test(this.username)) {
        this.usernameError = "学号/工号格式不正确，请输入8 - 12位数字。"
        return
      } else {
        this.usernameError = ''
      }

      // 基础验证
      if (!this.username || !this.pwd) {
        this.$message.warning('请输入用户名和密码')
        return
      }

      this.loading = true

      try {
        const response = await this.$axios.post('/api/login/', {
          username: this.username,
          password: this.pwd,
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.data.token) {
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('userInfo', JSON.stringify({
            id: response.data.id,
            username: response.data.username,
            role: response.data.role,
            real_name: response.data.real_name
          }))
          // 强制更新Vuex状态
          this.$store.commit('user/SET_INIT_STATE', {
            _init: true,
            id: response.data.id,
            role: response.data.role.toLowerCase(),
            isAuthenticated: true,
            real_name: response.data.real_name
          })
          const roleBasedRoutes = {
            'student': '/student/dashboard',
            'staff': '/staff/dashboard',
            'admin': '/admin/dashboard'
          }
          console.log('提交后Vuex状态:', JSON.parse(JSON.stringify(this.$store.state.user)))
          console.log('跳转前的角色:', response.data.role)
          console.log('目标路径:', roleBasedRoutes[response.data.role])
          console.log('[登录成功] 保存的UserInfo:', localStorage.getItem('userInfo'))
          console.log('[路由目标] 应跳转至:', `/${response.data.role}/dashboard`)
          // 添加状态变更监听
          this.$nextTick(() => {
            console.log('提交Store后的用户状态:', JSON.parse(JSON.stringify(this.$store.state.user)))
            console.log('本地存储Token:', !!localStorage.getItem('token'))
            console.log('本地用户信息:', localStorage.getItem('userInfo'))
          })
          // ↓ 合并为单一通知（调整文案内容）
          this.$message({
            message: `${response.data.real_name}，欢迎进入系统`,  // ← 建议使用真实姓名
            type: 'success',
            duration: 1500
          })

          await this.$router.push({path: `/${response.data.role}/dashboard`})

        } else {
          this.$message.error('服务器返回异常格式')
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail ||
            error.response?.data?.error ||
            '登录请求失败，请检查网络连接'
        this.$message.error(errorMsg)
        // 清空密码字段
        if (error.response?.status === 401) {
          this.pwd = ''
        }
      } finally {
        this.loading = false
      }
    },
  }
}
</script>

<style scoped>

#back_count {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
  url("../../assets/login.png") center/cover fixed;
}

.login-cont {
  width: 90%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.login-cont:hover {
  transform: translateY(-3px);
}

.login-cont h2 {
  margin-bottom: 2rem;
}
</style>