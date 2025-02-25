<template>
  <div>
    <el-tabs v-model="activeTab" type="card">
      <el-tab-pane label="注册" name="register">
        <el-form :model="registerForm" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="registerForm.username"></el-input>
          </el-form-item>
          <el-form-item label="学号/工号">
            <el-input v-model="registerForm.idNumber"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input type="password" v-model="registerForm.password"></el-input>
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="registerForm.role">
              <el-option label="学生" value="student"></el-option>
              <el-option label="教职工" value="staff"></el-option>
              <el-option label="管理员" value="admin"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister">注册</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="登录" name="login">
        <el-form :model="loginForm" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="loginForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input type="password" v-model="loginForm.password"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin">登录</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'register',
      registerForm: {
        username: '',
        idNumber: '',
        password: '',
        role: 'student'
      },
      loginForm: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    handleRegister() {
      // 这里发送注册请求到后端
      console.log('注册信息:', this.registerForm);
    },
    handleLogin() {
      // 这里发送登录请求到后端
      console.log('登录信息:', this.loginForm);
    }
  }
};
</script>