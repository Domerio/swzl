<template>
  <div id="backcont">
    <div class="login-cont">
      <h2>校园失物招领管理系统</h2>
      <div>
        <p>用户名</p>
        <el-input
            v-model="username"
            placeholder="请输入用户名"
            clearable
            @keyup.enter.native="handleLogin"></el-input>
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
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      // 基础验证
      if (!this.username || !this.pwd) {
        this.$message.warning('请输入用户名和密码')
        return
      }

      this.loading = true

      try {
        const response = await this.$axios.post('/api/login/', {
          username: this.username,
          password: this.pwd
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        })

        if (response.data.token) {
          this.$message.success('登录成功')

          // 存储认证信息
          localStorage.setItem('token', response.data.token)
          localStorage.setItem('userInfo', JSON.stringify({
            id: response.data.user_id,
            username: response.data.username
          }))

          // 提前存储用户名
          const username = response.data.username

          // 清除之前的定时器
          if (this.loginTimer) clearTimeout(this.loginTimer)

          this.loginTimer = setTimeout(() => {
            this.$message({
              message: `${username}，欢迎进入系统`,
              type: 'success',
              duration: 1500,
              onClose: () => {
                this.$router.push({name: 'Home'})
                    .then(() => console.log('路由跳转成功'))
                    .catch(err => {
                      console.error('路由跳转失败:', err)
                      this.$router.push('/') // 保底跳转
                    })
              }
            })
          }, 800)
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
    }
  }
}
</script>

<style scoped>
#backcont {
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
  color: #303133;
  font-size: 1.75rem;
  text-align: center;
}

.loginBtn {
  margin-top: 1.5rem;
  width: 100%;
}
</style>
