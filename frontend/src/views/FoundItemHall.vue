<template>
  <div class="lost-item-hall">
    <h1>🔍 失物大厅</h1>
    <el-table
      :data="lostItems"
      v-loading="loading"
      :header-cell-style="{ background: '#f8f9fa' }"
    >
      <template #empty>
        <div class="empty-state">
          <i class="el-icon-document-remove"></i>
          <span>当前没有可显示的失物信息</span>
        </div>
      </template>
      <el-table-column prop="title" label="物品名称" min-width="180">
        <template #default="{ row }">
          <span class="text-ellipsis">{{ row.title }}</span>
        </template>
      </el-table-column>
      <el-table-column label="类型" width="100">
        <template #default="{ row }">
          {{ getItemTypeLabel(row.item_type) }}
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" width="120">
        <template #default="{ row }">
          <el-tag effect="plain">{{ row.category }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="丢失时间" width="150">
        <template #default="{ row }">
          {{ formatTime(row.lost_time) }}
        </template>
      </el-table-column>
      <el-table-column label="丢失地点" width="200">
        <template #default="{ row }">
          {{ row.location }}
          <div
            v-if="row.location_lat && row.location_lng"
            class="detail-map-container"
            :id="'detail-map-' + row.id"
          ></div>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag
            :type="statusTypeMap[row.status]"
            effect="light"
            class="status-tag"
          >
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="viewDetails(row)">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 失物详情弹窗 -->
    <el-dialog
      title="🔍 物品详情"
      :visible.sync="detailDialogVisible"
      width="800px"
      custom-class="item-detail-dialog"
    >
      <el-row :gutter="20">
        <!-- 图片轮播区 -->
        <el-col :span="8">
          <el-carousel
            :interval="5000"
            height="300px"
            arrow="always"
          >
            <el-carousel-item
              v-for="(img, index) in currentItem.images"
              :key="index"
            >
              <el-image
                :src="img"
                fit="cover"
                class="detail-image"
              >
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
            </el-carousel-item>
          </el-carousel>
        </el-col>
        <!-- 详细信息区 -->
        <el-col :span="16">
          <el-descriptions
            :column="2"
            border
            label-class-name="detail-label"
          >
            <el-descriptions-item label="物品名称">{{ currentItem.title }}</el-descriptions-item>
            <el-descriptions-item label="物品分类">
              {{ currentItem.category_name }}
            </el-descriptions-item>
            <el-descriptions-item label="丢失时间">
              {{ formatTime(currentItem.lost_time) }}
            </el-descriptions-item>
            <el-descriptions-item label="丢失地点">
              {{ currentItem.location }}
              <div
                v-if="currentItem.location_lat && currentItem.location_lng"
                class="detail-map-container"
                :id="'detail-map-' + currentItem.id"
              ></div>
            </el-descriptions-item>
            <el-descriptions-item label="发布类型">
              {{ currentItem.item_type === 'lost' ? '失物登记' : '招领登记' }}
            </el-descriptions-item>
            <el-descriptions-item label="当前状态">
              <el-tag :type="statusTypeMap[currentItem.status]" size="medium">
                {{ statusTextMap[currentItem.status] }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="登记时间">
              {{ formatTime(currentItem.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="详细描述" :span="2">
              <pre class="description-pre">{{ currentItem.description }}</pre>
            </el-descriptions-item>
            <el-descriptions-item label="物品照片" :span="2" v-if="currentItem.images?.length">
              <el-image
                v-for="(img, index) in currentItem.images"
                :key="index"
                :src="img"
                fit="cover"
                class="detail-image"
              />
            </el-descriptions-item>
          </el-descriptions>
        </el-col>
      </el-row>
      <span slot="footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      lostItems: [],
      loading: false,
      detailDialogVisible: false,
      currentItem: {},
      statusTypeMap: {
        pending: 'warning',
        active: 'primary',
        completed: 'success',
        expired: 'info'
      },
      statusTextMap: {
        pending: '待审核',
        active: '进行中',
        completed: '已完成',
        expired: '已过期'
      }
    };
  },
  methods: {
    getItemTypeLabel(itemType) {
      return itemType === 'lost' ? '失物登记' : '招领登记';
    },
    formatTime(time) {
      // 这里可以添加具体的时间格式化逻辑
      return time;
    },
    async fetchLostItems() {
      this.loading = true;
      try {
        const response = await axios.get('/api/items/lost/');
        this.lostItems = response.data;
      } catch (error) {
        console.error('获取失物信息失败', error);
      } finally {
        this.loading = false;
      }
    },
    viewDetails(item) {
      this.currentItem = item;
      this.detailDialogVisible = true;
    }
  },
  mounted() {
    this.fetchLostItems();
  }
};
</script>

<style lang="scss" scoped>
.lost-item-hall {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);

  h1 {
    text-align: center;
    color: #303133;
    font-size: 28px;
    margin-bottom: 40px;
    position: relative;

    &::after {
      content: '';
      display: block;
      width: 60px;
      height: 3px;
      background: #409EFF;
      margin: 12px auto 0;
      border-radius: 2px;
    }
  }
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #606266;
}

.text-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-image {
  width: 150px;
  height: 150px;
  margin-right: 12px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  transition: transform 0.3s;

  &:hover {
    transform: scale(1.05);
    cursor: zoom-in;
  }
}

.description-pre {
  white-space: pre-wrap;
  line-height: 1.6;
  margin: 0;
  font-family: inherit;
}
</style>