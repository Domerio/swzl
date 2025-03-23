<template>
  <div class="lost-item-hall">
    <h1>🔍 招领大厅</h1>

    <!-- 添加搜索和筛选工具栏 -->
    <el-row :gutter="20" class="toolbar">
      <el-col :xs="24" :sm="12" :md="8" class="search-item">
        <el-input v-model="searchQuery" placeholder="物品名称/描述..." clearable class="search-input" @clear="handleFilter"
          @keyup.enter="handleFilter">
          <template #prefix>
            <i class="el-icon-search input-icon"></i>
          </template>
        </el-input>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8" class="search-item">
        <el-select v-model="filterType" placeholder="选择分类" clearable filterable class="type-selector"
          @change="handleFilter">
          <el-option v-for="item in categories" :key="item.value" :label="item.label" :value="item.value"
            :disabled="item.hasChildren">
            <span class="category-option" :style="{ paddingLeft: item.level * 20 + 'px' }">
              {{ item.label }}
              <i v-if="item.hasChildren" class="el-icon-folder-opened"></i>
            </span>
          </el-option>
        </el-select>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" class="search-item">
        <el-input v-model="locationQuery" placeholder="输入地址关键词..." clearable class="location-input"
          @clear="handleFilter" @keyup.enter="handleFilter">
          <template #prefix>
            <i class="el-icon-location-information input-icon"></i>
          </template>
          <template #append>
            <el-button type="primary" icon="el-icon-search" @click="handleFilter" />
          </template>
        </el-input>
      </el-col>
    </el-row>

    <el-table :data="filteredItems" v-loading="loading" :header-cell-style="{ background: '#f8f9fa' }">
      <template #empty>
        <div class="empty-state">
          <i class="el-icon-document-remove"></i>
          <span>当前没有可显示的招领信息</span>
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
          <el-tag effect="plain">{{ row.category_name }}</el-tag>
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
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template #default="{ row }">
          <el-tag :type="statusTypeMap[row.status]" effect="light" class="status-tag">
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

    <!-- 招领详情弹窗 -->
    <el-dialog title="🔍 物品详情" :visible.sync="detailDialogVisible" width="800px" custom-class="item-detail-dialog">
      <el-row :gutter="20">
        <!-- 图片轮播区 -->
        <el-col :span="8">
          <el-carousel :interval="5000" height="300px" arrow="always">
            <el-carousel-item v-for="(img, index) in currentItem.images" :key="index">
              <el-image :src="img" fit="cover" class="detail-image">
                <div slot="error" class="image-error">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </el-image>
            </el-carousel-item>
          </el-carousel>
        </el-col>
        <!-- 详细信息区 -->
        <el-col :span="16">
          <el-descriptions :column="2" border label-class-name="detail-label">
            <el-descriptions-item label="物品名称">{{ currentItem.title }}</el-descriptions-item>
            <el-descriptions-item label="物品分类">
              {{ currentItem.category_name }}
            </el-descriptions-item>
            <el-descriptions-item label="提交人">
              <el-tooltip v-if="currentItem.user?.role === 'admin'" content="管理员账号">
                <i class="el-icon-s-custom"></i>
              </el-tooltip>
              {{ currentItem.user?.real_name || '匿名用户' }}
              <span v-if="currentItem.user" class="user-role-tag">
                ({{ roleMap[currentItem.user.role] }})
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="拾取时间">
              {{ formatTime(currentItem.lost_time) }}
            </el-descriptions-item>
            <el-descriptions-item label="拾取地点">
              {{ currentItem.location }}
              <div v-if="currentItem.location_lat && currentItem.location_lng" class="detail-map-container"
                :id="'detail-map-' + currentItem.id"></div>
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
          </el-descriptions>
        </el-col>
      </el-row>
      <span slot="footer">
        <el-button :type="bookmarked ? 'success' : 'primary'"
          :icon="bookmarked ? 'el-icon-star-off' : 'el-icon-star-on'" @click="handleBookmark">
          {{ bookmarked ? '已收藏' : '收藏物品' }}
        </el-button>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import dayjs from 'dayjs';

export default {
  /* eslint-disable no-undef */
  // 在data部分修改
  data() {
    return {
      // 新增过滤相关数据
      searchQuery: '',
      locationQuery: '',  // 新增地址搜索
      filterType: null,
      typeOptions: [], // 移除硬编码选项
      categories: [],  // 新增分类数据
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
      },
      bookmarked: false,
    };
  },
  methods: {
    formatTime(time) {
      return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
    },
    // 新增过滤处理方法
    handleFilter() {
      // 如果需要后端过滤，可以调用API：
      this.fetchLostItems(this.filterParams)
    },
    async fetchCategories() {
      try {
        const response = await axios.get('/api/found/categories/tree/');
        this.categories = this.convertToFlatOptions(response.data);
      } catch (error) {
        console.error('获取分类失败', error);
      }
    },
    convertToFlatOptions(tree) {
      const flatten = (items) => {
        return items.reduce((acc, item) => {
          acc.push({
            value: item.id,
            label: item.name,
            hasChildren: item.children && item.children.length > 0
          });
          if (item.children) {
            acc.push(...flatten(item.children));
          }
          return acc;
        }, []);
      };
      return flatten(tree);
    },
    // 修改原有的获取数据方法以支持参数
    async fetchLostItems() {
      this.loading = true
      try {
        const response = await axios.get('/api/public/found-items/', {
          headers: {
            'Authorization': `Token ${this.$store.state.token}`,
            'X-CSRFToken': this.getCSRFToken()
          }
        })
        this.lostItems = response.data
      } catch (error) {
        console.error('获取招领信息失败', error)
      } finally {
        this.loading = false
      }
    },
    async checkBookmarkStatus() {
      try {
        // 修改请求路径为后端实际接口路径
        const response = await axios.get(`/api/bookmarks/${this.currentItem.id}/`, {
          headers: {
            'Authorization': `Token ${this.$store.state.token}`,
            'X-CSRFToken': this.getCSRFToken(),
          }
        });
        this.bookmarked = response.data.bookmarked;
      } catch (error) {
        console.error('获取收藏状态失败', error);
      }
    },
    getCSRFToken() {
      const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || '';
      return cookieValue;
    },
    async handleBookmark() {
      try {
        const config = {
          headers: {
            'Authorization': `Token ${this.$store.state.token}`,
            'X-CSRFToken': this.getCSRFToken(),
            'Content-Type': 'application/json'
          }
        };

        // 修正参数顺序（DELETE方法第二个参数是config）
        const method = this.bookmarked ? 'delete' : 'post';
        await axios[method](
          `/api/bookmarks/${this.currentItem.id}/`,
          method === 'delete' ? config : null, // 仅DELETE需要config在第二个参数
          method === 'post' ? config : null         // POST需要空数据体
        );

        this.bookmarked = !this.bookmarked;
        this.$message.success(this.bookmarked ? '收藏成功' : '已取消收藏');
      } catch (error) {
        console.error('操作收藏失败', error);
        this.$message.error(`操作失败: ${error.response?.data?.error || '未知错误'}`);
      }
    },
    viewDetails(item) {
      if (!this.$store.state.token) {
        this.$message.warning('请先登录');
        return;
      }
      this.currentItem = item;
      this.detailDialogVisible = true;
      this.checkBookmarkStatus();
    },
    // 初始化详情地图
    initDetailMap() {
      if (!window.AMap) {
        this.$message.warning('地图资源正在加载，请稍候')
        return
      }
      const lng = parseFloat(this.currentItem.location_lng)
      const lat = parseFloat(this.currentItem.location_lat)
      if (isNaN(lng) || isNaN(lat)) return

      this.destroyDetailMap()

      const mapContainerId = `detail-map-${this.currentItem.id}`
      const mapContainer = document.getElementById(mapContainerId)
      if (!mapContainer) return

      this.detailMap = new AMap.Map(mapContainerId, {
        zoom: 17,
        center: [lng, lat],
        resizeEnable: true
      })

      // 实例化独立控件
      const scale = new AMap.Scale()
      const toolBar = new AMap.ToolBar({
        position: { bottom: '20px', right: '20px' }
      })

      // 逐个添加控件
      scale.addTo(this.detailMap)
      toolBar.addTo(this.detailMap)

      // 添加标记
      new AMap.Marker({
        position: [lng, lat],
        content: '<div class="location-pin">📍</div>',
        map: this.detailMap
      })
    },
    destroyDetailMap() {
      if (this.detailMap) {
        try {
          this.detailMap.destroy()
        } catch (e) {
          console.warn('地图销毁过程中出现警告:', e.message)
        }
        this.detailMap = null
      }
    },
    getItemTypeLabel(itemType) {
      return {
        'lost': '失物登记',
        'found': '招领登记'
      }[itemType] || '未知类型';
    },
  },
  mounted() {
    this.fetchCategories();
    this.fetchLostItems();
    if (!window.AMap) {
      const key = 'db70318a1cf1f196b2746f10cb9df826'
      const plugins = [
        'AMap.Scale',
        'AMap.ToolBar'
      ].join(',')
      const script = document.createElement('script')
      script.src = `https://webapi.amap.com/maps?v=2.0&key=${key}&plugin=${plugins}`
      script.onerror = () => {
        console.error('高德地图SDK加载失败')
      }
      document.head.appendChild(script)
    }
  },
  computed: {
    roleMap() {
      return {
        admin: '管理员',
        teacher: '教职工',
        student: '学生'
      }
    },
    // 添加过滤计算属性
    filteredItems() {
      const query = this.searchQuery.toLowerCase()
      const locationQuery = this.locationQuery.toLowerCase()
      return this.lostItems.filter(item =>
        (item.title.toLowerCase().includes(query) ||
          item.description.toLowerCase().includes(query)) &&
        (item.location.toLowerCase().includes(locationQuery)) &&
        (!this.filterType || item.category === this.filterType)
      )
    }

  },
  watch: {
    detailDialogVisible(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          if (this.currentItem.location_lat && this.currentItem.location_lng) {
            this.initDetailMap();
          }
        });
      } else {
        this.destroyDetailMap();
      }
    },
  },
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

// 添加详情地图样式
.detail-map-container {
  width: 100%;
  height: 200px;
  margin-top: 12px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;

  &::after {
    content: '高德地图提供支持';
    position: absolute;
    right: 5px;
    bottom: 5px;
    font-size: 10px;
    color: #666;
    background: rgba(255, 255, 255, 0.8);
    padding: 2px 5px;
    border-radius: 3px;
  }
}

// 标记点样式
.detail-marker {
  font-size: 24px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
  transform: translate(-12px, -24px);
}

.toolbar {
  margin-bottom: 20px;

  .search-item {
    padding: 8px;
  }
}

.search-input {
  ::v-deep .el-input__prefix {
    left: 8px; // 调整搜索图标左间距
    display: flex;
    align-items: center;
  }
}

.type-selector {
  width: 100%;

  ::v-deep .el-input__prefix {
    left: 8px;
    pointer-events: none; // 禁止点击图标触发输入
  }

  .category-option {
    i {
      margin-left: 8px;
      font-size: 14px; // 调整文件夹图标大小
      vertical-align: middle;
    }
  }
}

.location-input {
  ::v-deep .el-input__prefix {
    left: 8px;
    display: flex;
    align-items: center;
  }
}

.input-icon {
  margin-left: 0; // 移除原有左边距
  color: #409EFF;
  font-size: 16px; // 统一图标尺寸
}
</style>