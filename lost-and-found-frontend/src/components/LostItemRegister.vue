<template>
  <div>
    <el-form :model="lostForm" label-width="80px">
      <el-form-item label="物品名称">
        <el-input v-model="lostForm.itemName"></el-input>
      </el-form-item>
      <el-form-item label="丢失时间">
        <el-date-picker
          v-model="lostForm.lostTime"
          type="datetime"
          placeholder="选择丢失时间"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="丢失地点">
        <el-input v-model="lostForm.lostLocation"></el-input>
      </el-form-item>
      <el-form-item label="特征描述">
        <el-input type="textarea" v-model="lostForm.description"></el-input>
      </el-form-item>
      <el-form-item label="图片上传">
        <el-upload
          class="upload-demo"
          action="your-upload-url"
          :on-success="handleUploadSuccess"
          :before-upload="beforeUpload"
        >
          <el-button size="small" type="primary">点击上传</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitLostItem">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lostForm: {
        itemName: '',
        lostTime: '',
        lostLocation: '',
        description: '',
        image: null
      }
    };
  },
  methods: {
    handleUploadSuccess(response, file, fileList) {
      this.lostForm.image = response.data;
    },
    beforeUpload(file) {
      // 这里可以做文件类型、大小等验证
      return true;
    },
    submitLostItem() {
      // 这里发送失物登记请求到后端
      console.log('失物登记信息:', this.lostForm);
    }
  }
};
</script>