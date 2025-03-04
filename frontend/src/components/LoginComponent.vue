<template>
  <div id="backcont">
    <div class="login-cont">
      <h2>校园失物招领管理系统</h2>
      <div>
        <p>用户名</p>
        <el-input v-model="username" placeholder="请输入用户名"/>
      </div>
      <div>
        <p>密码</p>
        <el-input type="password" v-model="pwd" placeholder="请输入密码"/>
      </div>
      <!--绑定登录按钮-->
      <el-button class="loginBtn" type="primary" @click="handleLogin">登录</el-button>
    </div>
  </div>
</template>

<script>

import {ref} from "vue";
import axios from "axios";


export default {
  setup() {
    const username = ref("");
    const pwd = ref("");

    // 定义 handleLogin 方法
    const handleLogin = () => {
      // 发送登录请求
      axios.post('/api/login/', {username: username.value, password: pwd.value},)
          .then(response => {
            if (response.data.code === 200) {
              // 处理登录成功的逻辑，例如保存 token，跳转到首页等
              console.log("登录成功", response.data);
              // 保存 token 到 localStorage
              localStorage.setItem('token', response.data.data.token);
            } else {
              // 处理登录失败的逻辑，例如显示错误消息
              console.error("登录失败", response.data.message);
            }
          })
          .catch(error => {
            console.error("登录请求失败", error);
          });
    };

    return {
      username,
      pwd,
      handleLogin,
    };
  },
};


</script>

<style>

#backcont {
  min-height: 100vh;
  width: 100%;
  /* 引入背景图片 */
  background-image: url("../assets/login.png ");
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
}

.login-cont {
  width: 450px;
  /* height: 300px; */
  background: #fff;
  border-radius: 8px;
  /* 使盒子垂直水平居中 */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  /* 内填充 */
  padding: 30px 50px;
  box-sizing: border-box;
}

.login-cont h2 {
  font-size: 22px;
  /* 文字加粗 */
  font-weight: normal;
  /* 文字水平居中 */
  text-align: center;
}

.loginBtn {
  width: 100%;
  margin: 20px 0;
  line-height: 32px;
}

.login-cont p {
  line-height: 20px;
}
</style>
