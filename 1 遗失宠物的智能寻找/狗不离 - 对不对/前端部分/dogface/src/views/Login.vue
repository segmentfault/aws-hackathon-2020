<template>
  <div class="login">
    <el-card class="box-card">
      <div slot="header" class="clearfix" style="text-align: center;">
        <span>欢迎使用 DOG FACE</span>
      </div>
      <div>
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
          <el-form-item label="账号" prop="username">
            <el-input v-model="ruleForm.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item style="text-align: center;">
            <el-button type="primary" @click="submitForm('ruleForm')" style="margin-right: 5px">登录</el-button>
            <el-button @click="register" style="margin-left: 5px">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
  export default {
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      return {
        ruleForm: {
          username: '',
          pass: ''
        },
        rules: {
          username: [
            { required: true, message: '请输入账号', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          pass: [
            { validator: validatePass, trigger: 'blur', required: true }
          ],
        }
      };
    },
    methods: {
      register(){
        this.$router.push('/register');
      },
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$router.push('/main');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      }
    }
  }
</script>

<style scoped>
  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
  .demo-ruleForm{
    margin-right: 60px;
  }
  .login{
    position: absolute;
    margin: auto;
    top: 28%;
    right: 0;
    left: 34%;
    bottom: 0;
  }
</style>
