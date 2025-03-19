<template>
  <div class="lost-item-register">
    <h1>📝 失物登记</h1>

    <el-form
        :model="form"
        ref="formRef"
        label-width="120px"
        :rules="rules"
        label-position="top"
    >
      <!-- 表单项 -->
      <el-form-item label="物品标题" prop="title">
        <el-input
            v-model="form.title"
            placeholder="请输入物品名称（如：黑色华为手机）"
        />
      </el-form-item>

      <el-form-item label="详细描述" prop="description">
        <el-input
            type="textarea"
            :rows="4"
            v-model="form.description"
            placeholder="请尽可能详细描述物品特征（如：型号、特殊标记等）"
            show-word-limit
            maxlength="300"
        />
      </el-form-item>

      <!-- 日期选择 -->
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="丢失时间" prop="lost_time">
            <el-date-picker
                v-model="form.lost_time"
                type="datetime"
                format="yyyy-MM-dd HH:mm"
                value-format="yyyy-MM-ddTHH:mm"
                placeholder="选择具体时间"
            />

          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="丢失地点" prop="location">
            <el-input
                v-model="form.location"
                placeholder="例如：3号教学楼201教室"
            />
            <el-button
                type="primary"
                icon="el-icon-map-location"
                @click="showMapDialog"
                class="map-btn"
                plain
            >选择位置
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 分类选择 -->
      <el-form-item label="物品分类" prop="category">
        <el-select
            v-model="form.category"
            placeholder="请选择最匹配的分类"
            filterable
        >
          <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
          />
        </el-select>
      </el-form-item>

      <!-- 联系方式 -->
      <el-form-item label="联系方式" prop="contact">
        <el-input
            v-model="form.contact"
            placeholder="手机号或邮箱"
        />
      </el-form-item>

      <!-- 图片上传 -->
      <el-form-item label="物品照片">
        <el-upload
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-change="handleUploadSuccess"
            :file-list="form.images"
            :before-upload="beforeUpload"
        >
          <i class="el-icon-plus"/>
        </el-upload>
        <div class="el-upload__tip">
          支持上传 JPG/PNG 格式图片，单张不超过5MB
        </div>
      </el-form-item>

      <!-- 操作按钮 -->
      <el-form-item>
        <el-button
            type="primary"
            class="submit-btn"
            :loading="isSubmitting"
            @click="submitForm"
        >
          {{ isSubmitting ? '提交中...' : '立即登记' }}
        </el-button>
      </el-form-item>
    </el-form>
    <!-- 在模板底部添加此对话框 -->
    <el-dialog
        title="✅ 登记成功"
        :visible.sync="dialogVisible"
        width="700px"
        @closed="handleDialogClosed"
    >
      <el-descriptions
          :column="2"
          border
          label-class-name="detail-label"
      >
        <!-- 弹窗内容 -->
        <el-descriptions-item label="物品标题">{{ submittedItem.title }}</el-descriptions-item>
        <el-descriptions-item label="分类">
          {{ getCategoryName(submittedItem.category) }}
        </el-descriptions-item>
        <el-descriptions-item label="丢失时间">
          {{ submittedItem.lost_time }}
        </el-descriptions-item>
        <el-descriptions-item label="丢失地点">{{ submittedItem.location }}</el-descriptions-item>
        <el-descriptions-item label="联系方式" :span="2">
          <el-link type="primary">{{ submittedItem.contact }}</el-link>
        </el-descriptions-item>
        <el-descriptions-item label="详细描述" :span="2">
          <pre class="description-pre">{{ submittedItem.description }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="物品照片" :span="2" v-if="submittedItem.images?.length">
          <el-image
              v-for="(img, index) in submittedItem.images"
              :key="index"
              :src="img.url"
              fit="cover"
              class="detail-image"
          />
        </el-descriptions-item>
      </el-descriptions>
      <!-- 底部操作按钮 -->
      <span slot="footer">
      <el-button
          type="success"
          @click="handleConfirm"
      >
        打印回执 (Ctrl+P)
      </el-button>
      <el-button
          type="primary"
          @click="dialogVisible = false"
      >
        确定返回
      </el-button>
    </span>
    </el-dialog>
    <!-- 添加地图弹窗 -->
    <!-- 在地图弹窗中添加加载状态 -->
    <el-dialog
        title="请在地图上选择位置"
        :visible.sync="mapDialogVisible"
        width="80%"
    >
      <div id="map-container" style="height: 500px; position: relative;">
        <div v-if="mapLoading" class="map-loading">
          <i class="el-icon-loading"></i> 正在获取地址信息...
        </div>
      </div>
      <span slot="footer">
      <el-button @click="mapDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmLocation">确定</el-button>
    </span>
    </el-dialog>
  </div>

</template>


<script>
import axios from 'axios';

export default {
  /* eslint-disable no-undef */
  data() {
    return {
      // 新增手机号验证规则
      phoneRules: [
        {required: true, message: '请输入联系方式', trigger: 'blur'},
        {
          pattern: /^(1[3-9]\d{9}|[\w-]+@[\w-]+\.[\w-]+)$/,
          message: '请输入有效的手机号或邮箱',
          trigger: 'blur'
        }
      ],
      form: {
        title: '',
        description: '',
        lost_time: null,
        location: '',
        category: null,
        contact: '',
        images: [],
        location_lng: null, // 新增经度字段
        location_lat: null  // 新增纬度字段
      },
      categories: [],
      fileList: [],
      rules: {
        title: [
          {required: true, message: '请输入标题', trigger: 'blur'}
        ],
        description: [
          {required: true, message: '请输入详细描述', trigger: 'blur'}
        ],
        lost_time: [
          {required: true, message: '请选择丢失时间', trigger: 'change'}
        ],
        location: [
          {required: true, message: '请输入地点', trigger: 'blur'}
        ],
        category: [
          {required: true, message: '请选择物品分类', trigger: 'change'}
        ],
        contact: [
          {required: true, message: '请输入联系方式', trigger: 'blur'}
        ]
      },
      isSubmitting: false,
      dialogVisible: false,
      submittedItem: {}, // 存储服务器返回的完整数据
      printStyle: `
      @media print {
        body * { visibility: hidden; }
        .el-dialog { width: 210mm!important; visibility: visible; }
        .el-dialog__header, .el-dialog__footer { display: none; }
      }
    `,
      mapDialogVisible: false,
      selectedLocation: {
        lng: null,
        lat: null,
        address: ''
      },
      map: null,
      geocoder: null, // 高德地图的Geocoder对象
      mapLoading: false, // 新增地图加载状态
      marker: null,      // 地图标记对象
      infoWindow: null,   // 信息窗口对象
    }
  },
  mounted() {
    this.fetchCategories()
    // 添加安全配置
    window._AMapSecurityConfig = {
      securityJsCode: 'd43a12d0b69aeacd6f9016db9b366433'
    };
    if (!window.AMap) {
      const key = 'db70318a1cf1f196b2746f10cb9df826';
      const script = document.createElement('script');
      // 同时加载三个插件
      script.src = `https://webapi.amap.com/maps?v=2.0&key=${key}&plugin=AMap.Geocoder,AMap.ToolBar,AMap.Scale`;
      script.async = true;
      script.onload = () => {
        this.geocoder = new AMap.Geocoder({
          city: "全国",
          timeout: 5000 // 增加5秒超时
        });
        console.log('AMap SDK and all plugins loaded');
      };
      document.head.appendChild(script);
    }
  },
  methods: {
    // 新增地图相关方法
    showMapDialog() {
      this.mapDialogVisible = true;
      this.$nextTick(() => {
        this.initAMap();
      });
    },

    initAMap() {
      if (!window.AMap) return;
      // 山西师范大学（太原校区）坐标（经度112.5865，纬度37.8603）
      const targetLngLat = new AMap.LngLat(112.662198, 37.745788);
      // 初始化地图
      this.map = new AMap.Map('map-container', {
        zoom: 15,
        center: targetLngLat, // 设置中心点
        resizeEnable: true,
        securityJsCode: 'd43a12d0b69aeacd6f9016db9b366433', // 你的安全密钥
        useAMapUI: true, // 使用高德地图UI组件
      });

      // 添加地图控件
      this.map.addControl(new AMap.ToolBar({
        position: 'LT'  // 左上角
      }));
      this.map.addControl(new AMap.Scale({
        position: 'LB'  // 左下角
      }));

      // 初始化信息窗口
      this.infoWindow = new AMap.InfoWindow({
        offset: new AMap.Pixel(0, -30)
      });

      // 地图点击事件
      // 地图点击事件
      this.map.on('click', (e) => {
        try {
          this.mapLoading = true;

          // 清除旧标记
          if (this.marker) {
            this.map.remove(this.marker);
          }

          // 添加新标记
          this.marker = new AMap.Marker({
            position: e.lnglat,
            title: '选择的位置'
          });
          this.map.add(this.marker);

          // 自动居中
          this.map.setCenter(e.lnglat);

          // 获取地址信息（使用回调函数）
          const geocoder = new AMap.Geocoder();
          geocoder.getAddress(e.lnglat, (status, result) => {
            try {
              this.mapLoading = false;

              if (status === 'complete' && result.info === 'OK') {
                const address = result.regeocode.formattedAddress;
                this.selectedLocation = {
                  lng: e.lnglat.getLng(),
                  lat: e.lnglat.getLat(),
                  address: address
                };

                // 实时更新输入框
                this.form.location = address;

                // 显示信息窗口
                this.infoWindow.setContent(`<div class="map-info">
          <h4>已选择位置：</h4>
          <p>${address}</p>
        </div>`);
                this.infoWindow.open(this.map, e.lnglat);
              } else {
                console.error('地址解析失败:', result);
                this.$message.warning('无法获取该位置地址，请重新选择');
              }
            } catch (err) {
              console.error('地址解析异常:', err);
              this.$message.warning('地址解析服务异常');
            }
          });

        } catch (error) {
          this.mapLoading = false;
          console.error('地址解析异常:', error);
          this.$message.warning('位置选择过程发生错误');
        }
      });
    },

    // 修改后的确认方法
    confirmLocation() {
      if (!this.selectedLocation.address) {
        this.$message.warning('请先在地图上选择位置');
        return;
      } else {
        this.form.location = this.selectedLocation.address;
        // 确保赋值给form的经纬度字段
        this.form.location_lng = this.selectedLocation.lng;
        this.form.location_lat = this.selectedLocation.lat;
      }

      // 已经实时更新，这里只需要关闭弹窗
      this.mapDialogVisible = false;


      // 清除地图元素
      if (this.marker) {
        this.map.remove(this.marker);
      }
      this.infoWindow.close();
    },

    // 分类ID转名称（匹配用户原有分类数据）
    getCategoryName(categoryId) {
      return this.categories.find(item => item.id === categoryId)?.name || '未知分类'
    },

    // 处理弹窗关闭后的操作
    handleDialogClosed() {
      this.$router.go(-1) // 或自定义跳转逻辑
    },

    // 打印功能
    handleConfirm() {
      const printWindow = window.open('', '_blank')
      printWindow.document.write(`
      <style>${this.printStyle}</style>
      ${document.querySelector('.el-dialog').outerHTML}
    `)
      printWindow.print()
      printWindow.close()
    },

    async fetchCategories() {
      try {
        const response = await axios.get('/api/lost/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('获取物品分类失败:', error)
        this.$message.error('获取物品分类失败，请稍后重试。')
      }
    },
    // 优化后的提交方法
    async submitForm() {
      try {
        this.isSubmitting = true;
        // 统一提交数据（含图片）
        const formData = new FormData();
        Object.keys(this.form).forEach(key => {
          if (key !== 'images') {
            // 处理所有非图片字段（包含经纬度）
            const value = this.form[key];

            // 处理空值情况
            if (value === null || value === undefined) {
              formData.append(key, '');
            } else {
              formData.append(key, value);
            }
          }
        });
        // 添加图片文件
        this.form.images.forEach((file) => {
          formData.append('images', file.raw);
        });
        const response = await axios.post('/api/items/lost/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${this.$store.state.token}`
          }
        });
        // 保存服务器返回的完整数据
        this.submittedItem = {
          ...response.data,
          images: this.form.images // 保留前端临时预览图
        };

        // 清空表单（根据需求选择保留或清除）
        this.$refs.formRef.resetFields();
        this.form.images = [];

        this.dialogVisible = true; // 显示弹窗

        this.$message.success({
          message: '登记成功，3秒后自动跳转',
          duration: 3000
        });
      } catch (error) {
        const msg = error.response?.data?.detail || '提交失败，请检查网络连接';
        this.$message.error(msg);
      } finally {
        this.isSubmitting = false;
      }
    },

    // 增强的文件上传处理
    handleUploadSuccess(file) {
      if (!file || !file.raw) {
        this.$message.error('文件加载异常')
        return
      }
      try {
        // 显示10秒内有效的预览链接
        const previewUrl = URL.createObjectURL(file.raw)
        const fileData = {
          uid: file.uid,        // 必须包含uid
          name: file.name,
          status: 'ready',      // 手动管理状态
          percentage: 0,        // 进度条初始值
          url: previewUrl,
          raw: file.raw
        }

        this.form.images = [...this.form.images, fileData]
      } catch (error) {
        console.error('文件预览错误:', error)
        this.$message.error('不支持该文件类型')
      }
    },


    beforeUpload(file) {
      const isValidType = ['image/jpeg', 'image/png'].includes(file.type)
      const isLt5M = file.size / 1024 / 1024 < 5
      if (!isValidType) {
        this.$message.error('仅支持 JPG/PNG 格式')
        return false
      }
      if (!isLt5M) {
        this.$message.error('图片大小不能超过5MB')
        return false
      }
      return true
    },
  }
}
</script>

<style lang="scss" scoped>
// 配色方案
$primary-color: #409EFF;
$error-color: #F56C6C;
$success-color: #67C23A;
$text-primary: #303133;
$text-secondary: #606266;
$border-color: #EBEEF5;
$bg-color: #f6f8fa;

.lost-item-register {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);

  h1 {
    text-align: center;
    color: $text-primary;
    font-size: 28px;
    margin-bottom: 40px;
    position: relative;

    &::after {
      content: '';
      display: block;
      width: 60px;
      height: 3px;
      background: $primary-color;
      margin: 12px auto 0;
      border-radius: 2px;
    }
  }

  // 表单项聚焦状态
  .el-form-item {
    margin-bottom: 28px;

    &:hover {
      .el-form-item__label::before {
        color: $primary-color;
      }
    }
  }

  // 输入框样式优化
  .el-input, .el-textarea, .el-select {
    .el-input__inner, .el-textarea__inner {
      border-radius: 8px;
      transition: all 0.3s;

      &:focus {
        border-color: $primary-color;
        box-shadow: 0 0 8px rgba($primary-color, 0.2);
      }
    }
  }

  // 图片上传样式
  .el-upload {
    &__tip {
      color: $text-secondary;
      font-size: 12px;
      margin-top: 8px;
    }

    &-list {
      &__item {
        transition: all 0.3s;
        border-radius: 8px;

        &:hover {
          background-color: rgba($primary-color, 0.05);
        }
      }
    }
  }

  // 提交按钮
  .submit-btn {
    width: 100%;
    padding: 14px;
    font-size: 16px;
    letter-spacing: 1px;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba($primary-color, 0.3);
    }
  }

  // 响应式适配
  @media (max-width: 768px) {
    padding: 24px 16px;
    margin: 0 16px;

    h1 {
      font-size: 24px;
    }

    .el-form-item__label {
      text-align: left !important;
      margin-bottom: 8px;
    }
  }
}

// 图片预览样式
.image-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 16px;

  .preview-item {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 8px;
    overflow: hidden;
    transition: all 0.3s;

    &:hover {
      .delete-btn {
        opacity: 1;
      }
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .delete-btn {
      position: absolute;
      right: 4px;
      top: 4px;
      opacity: 0;
      padding: 4px;
      background: rgba(black, 0.6);
      border: none;
      transition: opacity 0.3s;

      i {
        color: white;
        font-size: 14px;
      }
    }
  }
}

// 在<style>标签中添加：
.el-dialog {
  border-radius: 12px;

  &__header {
    background: #f8f9fa;
    border-radius: 12px 12px 0 0;
    padding: 20px;
  }

  &__body {
    padding: 30px;
  }
}

.detail-label {
  width: 100px;
  text-align: justify;
  text-justify: inter-ideograph;
  font-weight: 500;

  &::after {
    content: "："
  }
}

.description-pre {
  white-space: pre-wrap;
  line-height: 1.6;
  margin: 0;
  font-family: inherit;
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

// 添加地图信息窗口样式
.map-info {
  padding: 10px;
  min-width: 200px;

  h4 {
    margin: 0 0 5px;
    color: #409EFF;
    font-size: 14px;
  }

  p {
    margin: 0;
    font-size: 12px;
    color: #666;
  }
}

// 地图加载状态提示
.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999;
  padding: 10px 20px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  border-radius: 4px;
}
</style>
