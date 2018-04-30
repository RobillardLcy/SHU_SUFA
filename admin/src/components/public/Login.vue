<template>
  <div class="Login">
    <v-content>
      <v-container fluid fill-height>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-24">
              <v-toolbar dark color="light-blue darken-4">
                <v-toolbar-title>社团管理平台登录</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
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
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn large color="light-blue darken-4" dark @click="login">登录</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data: () => ({
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
  },
  methods: {
    login: function () {
      if (this.$refs.loginForm.validate()) {
        let loginInfo = JSON.stringify({
          id: this.loginData.studentID,
          password: this.loginData.password
        })
        this.$axios.post('login/', loginInfo)
          .then(response => {
            if ('detail' in response.data) {
              if (response.data.detail === 0) {
                this.$cookie.set('id', this.loginData.studentID, { expires: 1 })
                this.$cookie.set('admin', true, { expires: 1 })
              } else if (response.data.detail === 15) {
                this.loginData.errorAlert = true
                this.loginData.error = '您不是社团骨干'
              } else if (response.data.detail === 2) {
                this.loginData.errorAlert = true
                this.loginData.error = '学号或密码错误'
              }
            }
          })
      }
    }
  }
}
</script>

<style lang="css">
</style>
