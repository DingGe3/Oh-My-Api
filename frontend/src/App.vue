<template>
  <div id="app">
    <header class="header">
      <h1 class="title">Oh My API</h1>
      <nav class="nav">
        <router-link to="/dashboard" v-if="isAuthenticated">统计数据</router-link>
        <router-link to="/login" v-if="!isAuthenticated">登录</router-link>
        <button v-if="isAuthenticated" @click="logout">退出登录</button>
      </nav>
    </header>
    <main class="main-view">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const isAuthenticated = ref(false)
const router = useRouter()

const checkAuth = () => {
  isAuthenticated.value = !!localStorage.getItem('token')
}

const logout = () => {
  localStorage.removeItem('token')
  isAuthenticated.value = false
  router.push('/login')
}

onMounted(checkAuth)
</script>

<style scoped>
#app {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  color: white;
  padding: 0 20px;
  flex-shrink: 0;
}

.main-view {
  flex-grow: 1;
  display: flex;
  min-height: 0;
  overflow: hidden;
}

.nav a, .nav button {
  margin-left: 15px;
  color: white;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
}

.title {
  font-size: 24px;
}

html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>
