<template>
  <el-card class="stat-card" :style="{ borderLeft: `4px solid ${color}` }">
    <div class="card-content">
      <el-icon :color="color" :size="36">
        <component :is="icon" />
      </el-icon>
      <div class="text">
        <div class="value">{{ value }}</div>
        <div class="title">{{ title }}</div>
      </div>
    </div>
  </el-card>
</template>
