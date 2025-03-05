<!--frontend/src/App.vue-->
<template>
  <div id="app">
<!--    <LoginComponent msg="Welcome to Your Vue.js App"/>-->
<!--&lt;!&ndash;    <HomeComponent/>&ndash;&gt;-->
    <router-view></router-view>
  </div>
</template>

<script>
// import LoginComponent from './views/Login/LoginComponent.vue'
// import HomeComponent from "@/views/Home/HomeComponent.vue";
export default {
  name: 'App',
  components: {
    // LoginComponent,
    // HomeComponent,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  //margin-top: 60px;
}
</style>
