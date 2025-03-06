<template>
  <div class="lost-item-register">
    <h1>失物登记</h1>
    <el-form :model="form" ref="formRef" label-width="120px">
      <el-form-item label="标题">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="详细描述">
        <el-input type="textarea" v-model="form.description"></el-input>
      </el-form-item>
      <el-form-item label="丢失时间">
        <el-date-picker
            v-model="form.lost_time"
            type="datetime"
            placeholder="选择丢失时间"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="地点">
        <el-input v-model="form.location"></el-input>
      </el-form-item>
      <el-form-item label="物品分类">
        <el-select v-model="form.category" placeholder="请选择物品分类">
          <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="form.contact"></el-input>
      </el-form-item>
      <el-form-item label="物品图片">
        <el-upload
            action="/api/upload/"
            :multiple="true"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            :file-list="fileList"
        >
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
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
      fileList: []
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
        this.$message.error('获取物品分类失败，请稍后重试。')
      }
    },
    async submitForm() {
      try {
        const response = await axios.post('/api/items/lost/', this.form)
        this.$message.success('失物信息已成功登记')
        await this.$router.push('/items/lost/list')
      } catch (error) {
        this.$message.error('提交失败，请检查输入信息。')
      }
    },
    handleUploadSuccess(response, file, fileList) {
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