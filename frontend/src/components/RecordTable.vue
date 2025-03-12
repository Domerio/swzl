<template>
  <el-table :data="data" style="width: 100%">
    <el-table-column prop="date" label="日期" width="120"></el-table-column>
    <el-table-column prop="type" label="类型" width="100">
      <template #default="{row}">
        <el-tag :type="row.type === '失物' ? 'danger' : 'success'">
          {{ row.type }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="item" label="物品名称"></el-table-column>
    <el-table-column prop="status" label="状态">
      <template #default="{row}">
        <status-badge :status="row.status" />
      </template>
    </el-table-column>
    <el-table-column label="操作" width="120">
      <template #default>
        <el-button type="text" size="small">详情</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
