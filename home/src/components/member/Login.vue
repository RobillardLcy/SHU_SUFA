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
export default {
  name: 'Login',
  data: () => ({
    valid: true,
    loginData: {
      errorAlert: false,
      error: null,
      visible: false,
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
  methods: {
    // 账户登录
    login: function () {
      if (this.$refs.loginForm.validate()) {
        let loginInfo = JSON.stringify({
          id: this.loginData.studentID,
          password: this.loginData.password
        })
        this.$axios.post('login/', loginInfo)
          .then(response => {
            if ('success' in response.data) {
              this.$cookie.set('id', this.loginData.studentID)
              if ('error' in response.data) {
                if (response.data.error === 2) {
                  // 用户手机未激活, 登录后重定向到激活界面
                  window.sessionStorage.setItem('active', true)
                  window.sessionStorage.setItem('auth', true)
                  this.$router.push('/register/auth')
                } else if (response.data.error === 3) {
                  window.sessionStorage.setItem('auth', true)
                }
                this.$emit('closeLoginDialog')
              } else {
                if (this.loginDialog) {
                  this.$emit('closeLoginDialog')
                } else {
                  this.$router.go(-1)
                }
              }
            } else if ('error' in response.data && response.data.error === 1) {
              // 用户未注册或密码错误
              this.loginData.errorAlert = true
              this.loginData.error = '学号错误或密码错误'
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
