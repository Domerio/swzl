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
                style="width: 100%;"
            />

          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="丢失地点" prop="location">
            <div class="location-input-wrapper">
              <el-input
                  v-model="form.location"
                  placeholder="例如：3号教学楼201教室"
              />
              <el-button
                  type="primary"
                  icon="el-icon-map-location"
                  @click="showMapDialog"
                  class="map-btn"
                  circle
              >
              </el-button>
            </div>
          </el-form-item>
        </el-col>
      </el-row>

      <!-- 分类选择 -->
      <el-form-item label="物品分类" prop="category" width="100%">
        <!-- 修改el-cascader的options绑定 -->
        <el-cascader
            v-model="form.category"
            :options="categoryTreeOptions"
            :props="{
              checkStrictly: true,
              expandTrigger: 'hover',
              emitPath: false
            }"
            placeholder="请选择最匹配的分类"
            style="width: 50%;"
            @change="handleCategoryChange"
        />


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
import AMapLoader from '@amap/amap-jsapi-loader';

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
      categoriesTree: [], // 新增一个用于存储树形结构数据的数组
      categoryTreeOptions: [], // 用于存储树形结构选项的数组
      categoryList: [], // 存储分类列表
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
    this.fetchCategories().then(() => {
      this.categoryTreeOptions = this.convertToCascaderOptions(this.categoriesTree)
    })
    window._AMapSecurityConfig = {
      securityJsCode: 'c684b8bc9a42d62c059edd9fee411dce'
    };
  },
  methods: {
    // 修改convertToCascaderOptions方法
    convertToCascaderOptions(data) {
      return data.map(item => ({
        value: item.id,
        label: item.name,
        children: item.children.length ? this.convertToCascaderOptions(item.children) : undefined
      }));
    },
    getCSRFToken() {
      const cookieValue = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1] || '';
      return cookieValue;
    },
    async fetchCategories() {
      try {
        const response = await axios.get('/api/lost/categories/tree/',
            {
              headers: {
                'Authorization': `Token ${this.$store.state.token}`,
                'X-CSRFToken': this.getCSRFToken(),
              }
            }
        );
        this.categoriesTree = response.data;
      } catch (error) {
        console.error('获取物品分类失败:', error);
      }
    },
    handleCategoryChange(value) {
      // 处理分类选择变化
      console.log('选择的分类:', value);
    },
    // 新增地图相关方法
    showMapDialog() {
      this.mapDialogVisible = true;
      this.$nextTick(() => {
        this.initAMap();
      });
    },

    async initAMap() {

      try {
        // 彻底清理所有地图相关实例
        this.cleanupMap();

        this.mapLoading = true;

        // 强制禁用缓存
        const loaderConfig = {
          key: '3958565d98f73366bc8f766bcc44cb66',
          version: '2.0',
          plugins: ['AMap.Geocoder', 'AMap.Scale', 'AMap.ToolBar'],
          securityJsCode: 'c684b8bc9a42d62c059edd9fee411dce',
          AMapUI: {
            version: '1.1',
            plugins: []
          },
          url: `https://webapi.amap.com/maps?v=2.0&key=db70318a1cf1f196b2746f10cb9df826&t=${Date.now()}`
        };

        // 加载前检查全局AMap对象
        if (window.AMap) {
          window.AMap = undefined;
          delete window.AMap;
        }

        // 增加加载超时处理
        const AMap = await Promise.race([
          AMapLoader.load(loaderConfig),
          new Promise((_, reject) =>
              setTimeout(() => reject(new Error('地图加载超时')), 5000)
          )
        ]);

        // 增加安全校验
        if (!AMap?.Map) {
          throw new Error('高德地图API加载异常');
        }
        // 初始化地图
        this.initMapCore(AMap);
        this.initMapComponents(AMap);

      } catch (error) {
        console.error('地图加载失败:', error);
        this.$message.error(`地图初始化失败: ${error.message}`);
        this.cleanupMap();
      } finally {
        this.mapLoading = false;
      }
    },
    cleanupMap() {
      // 销毁所有地图相关实例
      if (this.map) {
        this.map.destroy();
        this.map = null;
      }
      this.geocoder = null;
      this.marker = null;
      if (this.infoWindow) {
        this.infoWindow.close();
        this.infoWindow = null;
      }
    },
    initMapCore(AMap) {
      this.map = new AMap.Map('map-container', {
        zoom: 15,
        center: new AMap.LngLat(112.662198, 37.745788),
        resizeEnable: true,
        animateEnable: true,
        touchZoomCenter: 1,
      });
    },
    initMapComponents(AMap) {
      // 初始化地理编码器
      this.geocoder = new AMap.Geocoder({
        city: '全国',
        timeout: 5000,
        extensions: 'all'
      });

      // 添加控件
      this.map.addControl(new AMap.ToolBar({position: 'LT'}));
      this.map.addControl(new AMap.Scale({position: 'LB'}));

      // 自定义信息窗口
      this.infoWindow = new AMap.InfoWindow({
        offset: new AMap.Pixel(0, -30),
        isCustom: true,
        autoMove: true,
        closeWhenClickMap: true
      });

      // 绑定地图事件
      this.map.on('click', this.handleMapClick);
    },

    handleMapClick(e) {
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
        this.geocoder.getAddress(e.lnglat, (status, result) => {
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
              // <!-- 在handleMapClick中更新信息窗口内容 -->
              this.infoWindow.setContent(`
<div class="map-info">
  <div class="info-header">
    <i class="el-icon-location"></i>
    <h3>📍 已确认位置</h3>
  </div>
  <div class="info-content">
    <div class="address-line">
      <span class="label">详细地址：</span>
      <span class="value">${address}</span>
    </div>
    <div class="coordinate">
      <span class="lng">经度 ${e.lnglat.getLng().toFixed(6)}</span>
      <span class="lat">纬度 ${e.lnglat.getLat().toFixed(6)}</span>
    </div>
  </div>
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
      const category = this.categoryList.find(item => item.id === categoryId);
      return category ? category.name : '未知分类';
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
  },
  async created() {
    try {
      // 获取分类列表
      const response = await axios.get('/api/lost/categories/');
      this.categoryList = response.data;
    } catch (error) {
      console.error('获取分类列表失败:', error);
    }
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
// 更新地图信息窗口样式为纯白背景
::v-deep .map-info {
  $primary: #409EFF;
  $bg-color: #ffffff; // 修改为纯白背景
  $border-color: #dcdfe6;

  background: $bg-color;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba($primary, 0.2);
  min-width: 280px;
  padding: 0;
  overflow: hidden;

  .info-header {
    background: $bg-color; // 头部也改为白色背景
    padding: 12px 16px;
    border-bottom: 1px solid rgba($primary, 0.1);
    display: flex;
    align-items: center;

    i {
      color: $primary;
      font-size: 18px;
      margin-right: 8px;
    }

    h3 {
      margin: 0;
      font-size: 15px;
      color: darken($primary, 10%);
      font-weight: 600;
      letter-spacing: 0.5px;
    }
  }

  .info-content {
    padding: 16px;

    .address-line {
      display: flex;
      line-height: 1.5;
      margin-bottom: 12px;

      .label {
        flex-shrink: 0;
        color: #606266;
        font-weight: 500;
        width: 70px;
      }

      .value {
        color: #303133;
        font-weight: 600;
        word-break: break-all;
      }
    }

    .coordinate {
      background: rgba($primary, 0.05);
      border-radius: 6px;
      padding: 8px;
      font-size: 12px;
      display: flex;
      justify-content: space-between;

      span {
        color: #606266;
        padding: 4px 8px;
        background: rgba(white, 0.9);
        border-radius: 4px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);

        &.lng::before {
          content: "🌐 ";
        }

        &.lat::before {
          content: "📍 ";
        }
      }
    }
  }

  // 调整三角指示符颜色为白色
  &::before {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    border-width: 10px 8px 0;
    border-style: solid;
    border-color: $bg-color transparent transparent;
    filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.1));
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

.location-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;

  .location-input {
    flex: 1;
    // 调整右侧留出按钮空间
    margin-right: 8px;
    // 调整输入框右侧圆角以配合按钮圆角
    ::v-deep .el-input__inner {
      border-top-right-radius: 0;
      border-bottom-right-radius: 0;
    }
  }

  .map-btn {
    // 使按钮尺寸与输入框高度一致
    width: 40px;
    height: 40px;
    padding: 8px;
    border-radius: 0 4px 4px 0;
    transition: all 0.3s;
    // 隐藏文字（兼容旧浏览器）
    span {
      display: none;
    }

    // 调整图标位置
    i {
      font-size: 20px;
      margin-left: -2px;
    }

    &:hover {
      transform: scale(1.05);
      box-shadow: 0 2px 8px rgba($primary-color, 0.2);
    }

    &:active {
      transform: scale(0.95);
    }
  }

  @media (max-width: 768px) {
    .map-btn {
      width: 36px;
      height: 36px;

      i {
        font-size: 18px;
      }
    }
  }
}

.el-cascader {
  input[aria-hidden="true"] {
    display: none !important;
  }

  .el-radio:focus:not(.is-focus):not(:active):not(.is-disabled) .el-radio__inner {
    box-shadow: none;
  }
}
</style>
