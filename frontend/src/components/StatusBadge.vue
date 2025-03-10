<!-- components/StatusBadge.vue -->
<template>
  <el-tag :type="statusType" size="small">
    {{ statusLabel }}
  </el-tag>
</template>

<script>
const statusMap = {
  pending: { label: '待审核', type: 'warning' },
  active: { label: '进行中', type: 'success' },
  completed: { label: '已完成', type: 'info' },
  expired: { label: '已过期', type: 'danger' }
}

export default {
  props: ['status'],
  computed: {
    statusLabel() {
      return statusMap[this.status]?.label || '未知状态'
    },
    statusType() {
      return statusMap[this.status]?.type || 'info'
    }
  }
}
</script>
