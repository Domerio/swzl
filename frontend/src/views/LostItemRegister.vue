<template>
  <div class="lost-item-register">
    <h1>失物登记</h1>
    <el-form :model="form" ref="formRef" label-width="120px" :rules="rules">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="详细描述" prop="description">
        <el-input type="textarea" v-model="form.description"></el-input>
      </el-form-item>
      <el-form-item label="丢失时间" prop="lost_time">
        <el-date-picker
          v-model="form.lost_time"
          type="datetime"
          placeholder="选择丢失时间"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="地点" prop="location">
        <el-input v-model="form.location"></el-input>
      </el-form-item>
      <el-form-item label="物品分类" prop="category">
        <el-select v-model="form.category" placeholder="请选择物品分类">
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="联系方式" prop="contact">
        <el-input v-model="form.contact"></el-input>
      </el-form-item>
      <el-form-item label="物品图片">
        <el-upload
          action="/api/upload/"
          :multiple="true"
          :on-success="handleUploadSuccess"
          :before-upload="beforeUpload"
          :file-list="fileList"
          :disabled="isSubmitting"
        >
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="isSubmitting">
          提交
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        title: '',
        description: '',
        lost_time: null,
        location: '',
        category: null,
        contact: '',
        images: []
      },
      categories: [],
      fileList: [],
      rules: {
        title: [
          { required: true, message: '请输入标题', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入详细描述', trigger: 'blur' }
        ],
        lost_time: [
          { required: true, message: '请选择丢失时间', trigger: 'change' }
        ],
        location: [
          { required: true, message: '请输入地点', trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择物品分类', trigger: 'change' }
        ],
        contact: [
          { required: true, message: '请输入联系方式', trigger: 'blur' }
        ]
      },
      isSubmitting: false
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await axios.get('/api/categories/')
        this.categories = response.data
      } catch (error) {
        console.error('获取物品分类失败:', error)
        this.$message.error('获取物品分类失败，请稍后重试。')
      }
    },
    async submitForm() {
      this.$refs.formRef.validate(async (valid) => {
        if (valid) {
          this.isSubmitting = true
          try {
            await axios.post('/api/items/lost/', this.form)
            this.$message.success('失物信息已成功登记')
            await this.$router.push('/items/lost/list')
          } catch (error) {
            console.error('提交失物信息失败:', error)
            if (error.response && error.response.data) {
              const errorMessage = Object.values(error.response.data).flat().join(', ')
              this.$message.error(`提交失败: ${errorMessage}`)
            } else {
              this.$message.error('提交失败，请检查输入信息。')
            }
          } finally {
            this.isSubmitting = false
          }
        } else {
          this.$message.error('请填写完整且正确的信息')
        }
      })
    },
    handleUploadSuccess(response) {
      this.form.images.push(response.url)
    },
    beforeUpload(file) {
      const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png'
      if (!isJpgOrPng) {
        this.$message.error('只能上传 JPG/PNG 格式的图片！')
      }
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        this.$message.error('图片大小不能超过 2MB！')
      }
      return isJpgOrPng && isLt2M
    }
  }
}
</script>

<style scoped>

</style>