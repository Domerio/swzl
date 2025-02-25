<template>
  <div>
    <el-form :model="foundForm" label-width="80px">
      <el-form-item label="物品名称">
        <el-input v-model="foundForm.itemName"></el-input>
      </el-form-item>
      <el-form-item label="拾取时间">
        <el-date-picker
          v-model="foundForm.foundTime"
          type="datetime"
          placeholder="选择拾取时间"
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="拾取地点">
        <el-input v-model="foundForm.foundLocation"></el-input>
      </el-form-item>
      <el-form-item label="特征描述">
        <el-input type="textarea" v-model="foundForm.description"></el-input>
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="foundForm.contactInfo"></el-input>
      </el-form-item>
      <el-form-item label="匿名发布">
        <el-switch v-model="foundForm.isAnonymous"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFoundItem">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      foundForm: {
        itemName: '',
        foundTime: '',
        foundLocation: '',
        description: '',
        contactInfo: '',
        isAnonymous: false
      }
    };
  },
  methods: {
    submitFoundItem() {
      // 这里发送招领登记请求到后端
      console.log('招领登记信息:', this.foundForm);
    }
  }
};
</script>