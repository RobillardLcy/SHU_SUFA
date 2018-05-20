<template lang="html">
  <div class="Login">
    <v-card class="text-xs-center" max-width=500>
      <v-toolbar dark color="light-blue darken-4">
        <v-toolbar-title>登录</v-toolbar-title>
      </v-toolbar>
      <v-alert
        type="error"
        v-model="loginData.errorAlert"
        transition="fade-transition"
        dismissible
        >{{ loginData.error }}</v-alert>
      <v-container>
        <v-form v-model="valid" ref="loginForm" lazy-validation>
          <v-text-field
            prepend-icon="person"
            label="学号"
            :rules="loginData.studentIDRules"
            v-model="loginData.studentID"
            required></v-text-field>
          <v-text-field
            prepend-icon="lock"
            label="密码"
            :rules="loginData.passwordRules"
            v-model="loginData.password"
            :append-icon="loginData.visible ? 'visibility_off' : 'visibility'"
            :append-icon-cb="() => (loginData.visible = !loginData.visible)"
            :type="loginData.visible ? 'text' : 'password'"
            @keyup.enter="loginTest"
            required></v-text-field>
          <!-- TODO: 验证码 -->
          <v-btn large color="primary" dark @click="login">登录</v-btn>
          <v-btn large color="green" dark @click="register">社团注册</v-btn>
        </v-form>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import { JSEncrypt } from 'jsencrypt'
export default {
  name: 'Login',
  data: () => ({
    valid: true,
    loginData: {
      errorAlert: false,
      error: null,
      visible: false,
      publicKey: null,
      studentID: null,
      studentIDRules: [
        (v) => !!v || '学号不能为空'
      ],
      password: null,
      passwordRules: [
        (v) => !!v || '密码不能为空'
      ]
    }
  }),
  props: {
    loginDialog: {
      type: Boolean,
      default () {
        return false
      }
    }
  },
  mounted: function () {
    this.getKey()
  },
  methods: {
    // 获取公钥
    getKey: function () {
      this.$axios.get('member/login/')
        .then(response => {
          this.loginData.publicKey = response.data.public_key
        })
        .catch(error => {
          console.log(error)
          window.alert('网络出错，请刷新页面重试！')
        })
    },
    // 账户登录
    login: function () {
      if (this.$refs.loginForm.validate()) {
        let timestamp = Date.now()
        let encrypt = new JSEncrypt()
        encrypt.setPublicKey(this.loginData.publicKey)
        let content = encrypt.encrypt(timestamp + this.loginData.studentID + this.loginData.password)
        let loginInfo = JSON.stringify({
          id: this.loginData.studentID,
          password: this.loginData.password,
          content: content
        })
        this.$axios.post('member/login/', loginInfo)
          .then(response => {
            if ('detail' in response.data) {
              if (response.data.detail === 0 || response.data.detail === 3 || response.data.detail === 4) {
                this.$cookie.set('id', this.loginData.studentID, { expires: 1 })
                if (response.data.detail === 0) {
                  this.$cookie.set('college', response.data.college.id)
                  window.localStorage.setItem('college', JSON.stringify(response.data.college))
                  if ('team' in response.data) {
                    this.$cookie.set('team', response.data.team.id)
                    window.localStorage.setItem('team', JSON.stringify(response.data.team))
                    this.$emit('loginSuccess')
                  } else {
                    this.$emit('loginSuccess')
                  }
                } else if (response.data.detail === 3) {
                  window.sessionStorage.setItem('auth', true)
                  this.$cookie.set('mobile', response.data.mobile)
                  this.$router.push('/register')
                } else if (response.data.detail === 4) {
                  window.sessionStorage.setItem('auth', true)
                }
                if (this.loginDialog) {
                  this.$emit('closeLoginDialog')
                } else {
                  this.$router.go(-1)
                }
              } else if (response.data.detail === 2) {
                this.loginData.errorAlert = true
                this.loginData.error = '学号或密码错误'
              }
            } else {
              this.loginData.errorAlert = true
              this.loginData.error = '网络错误，请重试'
            }
          })
          .catch(error => {
            console.log(error)
            this.loginData.errorAlert = true
            this.loginData.error = '网络错误，请重试'
          })
      }
    },
    // 用户注册页面跳转
    register: function () {
      this.$router.push('/register')
      this.$emit('closeLoginDialog')
    }
  }
}
</script>

<style lang="css">
</style>
