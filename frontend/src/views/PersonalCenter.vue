<template>
  <div class="personal-center">
    <h1>个人中心 - 欢迎 {{ user.real_name }}</h1>
    <!-- 历史发布记录 -->
    <h2>历史发布记录</h2>
    <ul>
      <li v-for="record in lostAndFoundRecords" :key="record.id">
        {{ record.title }} - {{ record.get_status_display() }}
      </li>
    </ul>
    <!-- 收藏信息 -->
    <h2>收藏信息</h2>
    <ul>
      <li v-for="bookmark in bookmarks" :key="bookmark.id">
        {{ bookmark.item.title }}
      </li>
    </ul>
    <!-- 消息通知 -->
    <h2>消息通知</h2>
    <ul>
      <li v-for="notification in notifications" :key="notification.id">
        {{ notification.content }} - {{ notification.get_notification_type_display() }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      user: this.$store.state.user.info,
      lostAndFoundRecords: [],
      bookmarks: [],
      notifications: []
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const [recordsRes, bookmarksRes, notificationsRes] = await Promise.all([
          axios.get('/api/items/history/', { params: { user_id: this.user.id } }),
          axios.get('/api/bookmarks/', { params: { user_id: this.user.id } }),
          axios.get('/api/notifications/', { params: { user_id: this.user.id } })
        ])
        this.lostAndFoundRecords = recordsRes.data
        this.bookmarks = bookmarksRes.data
        this.notifications = notificationsRes.data
      } catch (error) {
        this.$message.error('获取数据失败，请稍后重试。')
      }
    }
  }
}
</script>

<style scoped>

</style>