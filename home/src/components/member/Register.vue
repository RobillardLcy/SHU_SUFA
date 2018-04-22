<template lang="html">
  <div class="Register">
    <v-stepper :value="step">
      <v-stepper-header>
        <v-stepper-step step="1">学号认证</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="2">社团注册</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="3">手机验证</v-stepper-step>
      </v-stepper-header>
      <v-stepper-items>
          <v-stepper-content :step="1">
            <v-flex md6 offset-md3 text-xs-center>
              <h1>学号认证</h1>
              <v-form v-model="certificate.valid" ref="certificateForm" lazy-validation>
                <v-text-field
                  label="学号"
                  v-model="certificate.studentID"
                  :rules="certificate.studentIDRules"
                  required></v-text-field>
                <v-text-field label="学生证密码"
                  v-model="certificate.password"
                  :rules="certificate.passwordRules"
                  :append-icon="certificate.visible ? 'visibility_off' : 'visibility'"
                  :append-icon-cb="() => (certificate.visible = !certificate.visible)"
                  hint="6位~32位"
                  :type="certificate.visible ? 'text' : 'password'"
                  required></v-text-field>
                <v-btn
                  color="primary"
                  @click="cer()">认证</v-btn>
              </v-form>
            </v-flex>
          </v-stepper-content>
        <v-container text-xs-center>
          <v-stepper-content :step="2" class="text-xs-center">
            <h1>社团注册</h1>
            <v-form v-model="register.valid" ref="registerForm" lazy-validation>
              <v-text-field
                label="学号"
                :value="certificate.studentID"
                disabled
                v-show="$vuetify.breakpoint.width < 1264"></v-text-field>
              <v-text-field
                label="姓名"
                :value="register.studentName"
                disabled
                v-show="$vuetify.breakpoint.width < 1264"></v-text-field>
              <v-layout row justify-space-between v-show="$vuetify.breakpoint.width < 1264">
                <v-flex xs5>
                  <v-select
                    label="性别"
                    :items="genderChoices"
                    :rules="register.genderRules"
                    v-model="register.gender"
                    required></v-select>
                </v-flex>
                <v-flex xs5>
                  <v-select
                    label="校区"
                    :items="campusChoices"
                    :rules="register.campusRules"
                    v-model="register.campus"
                    required></v-select>
                </v-flex>
              </v-layout>
              <v-layout row v-show="$vuetify.breakpoint.width >= 1264">
                <v-flex md2>
                  <v-text-field
                    label="学号"
                    :value="certificate.studentID"
                    disabled></v-text-field>
                </v-flex>
                <v-flex md5 offset-md1>
                  <v-text-field
                    label="姓名"
                    :value="register.studentName"
                    disabled></v-text-field>
                </v-flex>
              </v-layout>
              <v-layout row v-show="$vuetify.breakpoint.width >= 1264">
                <v-flex md2>
                  <v-select
                    label="性别"
                    :items="genderChoices"
                    :rules="register.genderRules"
                    v-model="register.gender"
                    required></v-select>
                </v-flex>
                <v-flex md2 offset-md1>
                  <v-select
                    label="校区"
                    :items="campusChoices"
                    :rules="register.campusRules"
                    v-model="register.campus"
                    required></v-select>
                </v-flex>
              </v-layout>
              <v-flex lg6>
                <v-select
                  label="学院"
                  :items="collegeChoices"
                  :rules="register.collegeRules"
                  v-model="register.college"
                  autocomplete
                  required></v-select>
              </v-flex>
              <v-flex md6 xs12>
                <v-text-field
                  label="电话"
                  :rules="register.mobileRules"
                  v-model="register.mobile"
                  required></v-text-field>
              </v-flex>
              <br/>
              <v-divider></v-divider>
              <br/>
              <v-flex lg6 md8>
                <v-text-field
                  label="密码"
                  :rules="register.passwordRules"
                  v-validate="'required'"
                  data-vv-name="password"
                  v-model="register.password"
                  :append-icon="register.visible ? 'visibility_off' : 'visibility'"
                  :append-icon-cb="() => (register.visible = !register.visible)"
                  :type="register.visible ? 'text' : 'password'"
                  hint="密码长度为6~32位"
                  required></v-text-field>
              </v-flex>
              <v-flex lg6 md8>
                <v-text-field
                  label="密码确认"
                  :error="register.password === register.passwordConfirm ? false : true"
                  :hint="register.password === register.passwordConfirm ? '' : '密码不一致'"
                  v-model="register.passwordConfirm"
                  type="password"
                  required></v-text-field>
              </v-flex>
              <br/>
              <v-divider></v-divider>
              <br/>
              <v-flex lg6 md8>
                <v-text-field
                  label="喜爱的球队"
                  v-model="register.favoriteClub"
                  :rules="[v => !!v || '请输入喜爱的球队']"
                  required></v-text-field>
              </v-flex>
              <!-- TODO: 收集新社团成员数据 -->
              <!-- <v-flex md2>
                <v-select
                  label="球龄"
                  :items="[{text:'小于两年',value:0},{text:'两年至十年',value:1},{text:'大于十年',value:2}]"
                  :v-model="register.experience"></v-select>
              </v-flex> -->
              <v-layout row justify-center>
                <v-flex xl1 md2 s3 xs6>
                  <v-checkbox
                    label="我同意"
                    v-model="register.contactAgree"
                    :rules="[v => !!v || '请阅读社团注册协议']"
                    required></v-checkbox>
                </v-flex>
                <v-flex xl1 md2 s3 xs6>
                  <v-dialog v-model="register.contact.active" persistent max-width=1000>
                    <v-btn color="primary" dark flat large slot="activator">注册协议</v-btn>
                    <v-card class="text-xs-center">
                      <v-card-title class="headline">上海大学足球协会注册协议</v-card-title>
                      <v-spacer></v-spacer>
                      <v-divider></v-divider>
                      <v-card-text>{{ register.contact.content }}</v-card-text>
                      <v-spacer></v-spacer>
                      <v-btn large color="green" flat @click.native="register.contact.active = false, register.contactAgree = true">同意</v-btn>
                      <v-btn large color="red" flat @click.native="register.contact.active = false">取消</v-btn>
                    </v-card>
                  </v-dialog>
                </v-flex>
              </v-layout>
              <v-btn
                color="success"
                @click="reg()">注册</v-btn>
            </v-form>
          </v-stepper-content>
        </v-container>
        <v-stepper-content :step="3" class="text-xs-center">
          <h1>手机验证</h1>
          <v-form v-model="authenticate.valid" ref="authenticateForm" lazy-validation>
            <v-btn
              color="primary"
              :disabled="!authenticate.valid"
              @click="auth()">提交</v-btn>
          </v-form>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data: () => ({
    step: 1,
    certificate: {
      valid: true,
      studentID: null,
      studentIDRules: [
        (v) => !!v || '学号不能为空'
      ],
      password: null,
      passwordRules: [
        (v) => !!v || '学生证密码不能为空'
      ],
      visible: false
    },
    genderChoices: [
      {
        text: '男',
        value: 'male'
      },
      {
        text: '女',
        value: 'female'
      }
    ],
    campusChoices: [
      {
        text: '宝山',
        value: 'BS'
      },
      {
        text: '延长',
        value: 'YC'
      },
      {
        text: '嘉定',
        value: 'JD'
      }
    ],
    collegeChoices: [],
    register: {
      valid: true,
      studentName: '',
      studentNameRules: [
        (v) => !!v || '姓名不能为空'
      ],
      gender: '',
      genderRules: [
        (v) => !!v || '性别不能为空'
      ],
      college: '',
      collegeRules: [
        (v) => !!v || '学院不能为空'
      ],
      campus: null,
      campusRules: [
        (v) => !!v || '校区不能为空'
      ],
      mobile: null,
      mobileRules: [
        (v) => !!v || '电话不能为空',
        (v) => (v && v.length === 11 && /^1[3|4|5|7|8][0-9]\d{4,8}$/.test(v)) || '电话不符合规范'
      ],
      password: null,
      passwordRules: [
        (v) => !!v || '密码不能为空',
        (v) => (v && v.length >= 6 && v.length <= 32) || '密码不符合要求, 长度为6~32位'
      ],
      visible: false,
      passwordConfirm: null,
      favoriteClub: null,
      foot: null,
      experience: null,
      contactAgree: false,
      // TODO: 足协加入协议由后端数据库调入
      contact: {
        active: false,
        content: ''
      }
    },
    authenticate: {
      active: true
    }
  }),
  mounted: function () {
    this.getColleges()
  },
  methods: {
    getColleges: function () {
      this.$axios.get('/colleges/list/')
        .then(response => {
          for (var i = 0; i < response.data.length; i++) {
            this.collegeChoices.push({
              text: response.data[i].name,
              value: response.data[i].id
            })
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    cer: function () {
      if (this.$refs.certificateForm.validate()) {
        let certificateData = JSON.stringify({
          studentID: this.certificate.studentID,
          password: this.certificate.password
        })
        this.$axios.post('authentication/', certificateData)
          .then(response => {
            if ('studentID' in response.data && 'studentName' in response.data) {
              if (response.data.studentID === this.certificate.studentID) {
                this.register.studentName = response.data.studentName
                this.step = 2
              } else {
                window.alert('认证失败！')
              }
            } else {
              window.alert('认证失败！')
            }
          })
          .catch(error => {
            console.log(error)
            window.alert('网络错误，请重试！')
          })
      }
    },
    reg: function () {
      if (this.$refs.registerForm.validate()) {
        let info = JSON.stringify({
          gender: this.register.gender,
          mobile: this.register.mobile,
          campus: this.register.campus,
          favorite_club: this.register.favoriteClub,
          password: this.register.password,
          college: this.register.college
        })
        this.$axios.post('register/', info)
          .then(response => {
            if ('detail' in response.data) {
              if (response.data.detail === 7) {
                window.alert('未认证或认证已失效！')
                this.step = 1
              } else if (response.data.detail === 8) {
                window.alert('注册出错，请重试！')
              }
            } else {
              this.$cookie.set('id', this.certificate.studentID, { expires: 14 })
              this.step = 3
            }
          })
          .catch(error => {
            console.log(error)
            window.alert('网络错误，请重试！')
          })
      }
    },
    auth: function () {
      // TODO: 验证手机号码
      if (this.$refs.authenticateForm.validate()) {

      }
    }
  }
}
</script>

<style lang="css">
</style>
