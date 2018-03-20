<template>
  <div id="home">
    <v-app>
      <v-navigation-drawer fixed :clipped="$vuetify.breakpoint.width > 1264" app v-model="drawer">
        <v-list dense>
          <v-list-group v-for="item in items" :value="item.active" :key="item.title">
            <v-list-tile slot="item" @click="" router :to="item.url">
              <v-list-tile-action>
                <v-icon>{{ item.action }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
              <v-list-tile-action v-if="item.items">
                <v-icon>keyboard_arrow_down</v-icon>
              </v-list-tile-action>
            </v-list-tile>
            <v-list-tile v-for="subItem in item.items" :key="subItem.title" router :to="subItem.url">
                <v-list-tile-action>
                  <v-icon>{{ subItem.action }}</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                  <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
        </v-list>
        <v-divider></v-divider>
        <v-subheader v-show="loginData.active">报名通道</v-subheader>
        <v-list dense>
          <v-list-tile v-for="activity in activities" :key="activity.title" router :to="activity.url">
            <v-list-tile-content>
              <v-list-tile-title>{{ activity.name }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-divider v-show="loginData.active"></v-divider>
        <v-subheader v-show="loginData.active">我的球队</v-subheader>
        <v-list dense>
          <v-list-tile v-for="team in teams" :key="team.name" router :to="team.url">
            <v-list-tile-content>
              <v-list-tile-title>{{ team.name }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-navigation-drawer>
      <v-toolbar color="light-blue darken-4" clipped-left fixed app>
        <v-toolbar-title
          :style="$vuetify.breakpoint.width > 1264 && 'width: 100px'"
          class="ml-0 pl-3"
          :class="$vuetify.breakpoint.width <= 1264 && 'pr-3'">
          <v-toolbar-side-icon dark @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        </v-toolbar-title>
        <a href="/"><img src="/static/logo/sufa_logo_website.png" alt="SUFA"></a>
        <v-spacer></v-spacer>
        <v-menu v-show="loginData.active" offset-x :nudge-width="150" v-model="menu">
          <v-btn color="light-blue darken-4" dark slot="activator">
            <v-icon left>account_circle</v-icon>
            {{ memberProfile.studentName }}
          </v-btn>
          <v-card>
            <v-list>
              <v-list-tile avatar>
                <v-list-tile-avatar>
                  <img :src="memberProfile.photo">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ memberProfile.studentID }}  {{ memberProfile.studentName }}</v-list-tile-title>
                  <v-list-tile-sub-title>{{ memberProfile.gender }}  {{ memberProfile.grade }}</v-list-tile-sub-title>
                  <v-list-tile-sub-title>{{ memberProfile.college }}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
            <v-divider></v-divider>
            <v-list>
              <v-card-actions>
                <v-btn flat small color="primary" to="/member">个人中心</v-btn>
                <v-spacer></v-spacer>
                <v-btn flat small color="red" @click="logout">注销</v-btn>
              </v-card-actions>
            </v-list>
          </v-card>
        </v-menu>
        <v-dialog v-show="!loginData.active" v-model="loginDialog" max-width=800>
          <v-btn color="light-blue darken-4" dark slot="activator">
            <v-icon left>account_circle</v-icon>
            登录
          </v-btn>
          <v-card class="text-xs-center">
            <v-toolbar dark color="light-blue darken-4">
              <v-toolbar-title>登录</v-toolbar-title>
            </v-toolbar>
            <v-container>
              <v-form>
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
                <v-btn large color="green" dark router :to="register" @click.native="loginDialog = false">社团注册</v-btn>
              </v-form>
            </v-container>
          </v-card>
        </v-dialog>
        <v-btn color="success" dark v-show="!loginData.active" router :to="register">
          社团注册
        </v-btn>
      </v-toolbar>
      <v-content>
        <v-container fluid>
          <router-view/>
        </v-container>
      </v-content>
      <v-footer app>
        <v-spacer></v-spacer>
        <div class="text-xs-center">
          © 2017-{{ new Date().getFullYear() }} <a href="https://www.shusufa.com">上海大学足球协会</a>&nbsp;&nbsp;&nbsp;&nbsp;社团所属学校：<a href="http://www.shu.edu.cn">上海大学</a>
          <br/>
          社团微信公众号：上大足协<br/>社团邮箱：shu_sufa@163.com
        </div>
        <v-spacer></v-spacer>
      </v-footer>
    </v-app>
  </div>
</template>

<script>
export default {
  name: 'home',
  data: () => ({
    drawer: null,
    loginDialog: false,
    menu: false,
    loginData: {
      active: false,
      visible: false,
      studentID: '',
      studentIDRules: [
        (v) => !!v || '学号不能为空'
      ],
      password: '',
      passwordRules: [
        (v) => !!v || '密码不能为空'
      ]
    },
    register: '/register',
    memberProfile: {
      studentID: '',
      studentName: '',
      gender: '',
      grade: '',
      college: '',
      photo: ''
    },
    // TODO: 网站导航栏可管理，即网站导航栏由后台数据库导入
    items: [
      {
        action: 'home',
        title: '主页',
        url: '/home'
      },
      {
        action: 'description',
        title: '简介',
        items: [
          { title: '社团简介', url: '/about/community' },
          { title: '指导老师', url: '/about/teacher' },
          { title: '主席团', url: '/about/president' },
          { title: '事务部', url: '/about/affair' },
          { title: '宣传部', url: '/about/publicity' },
          { title: '外联部', url: '/about/liaison' },
          { title: '财务部', url: '/about/finance' },
          { title: '技术部', url: '/about/technology' },
          { title: '裁判协会', url: '/about/referee' },
          { title: '校队经理', url: '/about/manager' }
        ]
      },
      {
        action: 'group',
        title: '队伍',
        items: [
          { title: '上海大学男子足球队', url: '/team/man_team' },
          { title: '上海大学女子足球队', url: '/team/woman_team' },
          { title: '年级梯队', url: '/team/grade_team' },
          { title: '自由队伍', url: '/team/free_team' }
        ]
      },
      {
        action: 'whatshot',
        title: '比赛',
        items: [
          { title: '上海大学学院杯', url: '/leagues/college_cup' },
          { title: '上海大学足球协会杯', url: '/leagues/association_cup' },
          { title: '上海大学足球协会新生杯', url: '/leagues/newStudent_cup' },
          { title: '自由组织赛事', url: '/leagues/free_leagues' }
        ]
      },
      {
        action: 'flag',
        title: '球迷会',
        items: [
          { title: '拜仁慕尼黑', url: '/fanClub/bayern' },
          { title: '巴塞罗那', url: '/fanClub/barca' },
          { title: '皇家马德里', url: '/fanClub/madrid' },
          { title: '曼彻斯特联', url: '/fanClub/manutd' }
        ]
      },
      {
        action: 'local_activity',
        title: '活动',
        url: '/activities'
      }
    ],
    // TODO: 活动从数据库中读取，动态更新
    activities: [
    ],
    // TODO: 队伍通过查询登录用户的信息，确认用户已加入的队伍显示，未加入这提供未加入队伍提示，并显示加入队伍的URL
    teams: [
    ]
  }),
  props: {
  },
  computed: {
  },
  methods: {
    // 账户登录
    login: function () {
      let loginInfo = JSON.stringify({
        id: this.loginData.studentID,
        password: this.loginData.password
      })
      this.$axios.post('login/', loginInfo)
      .then(response => {
        this.loginData.active = true
        this.loginDialog = false
      })
      .catch(error => {
        console.log(error)
      })
    },
    // 账户注销
    logout: function () {
      this.$axios.post('logout/')
      .then(response => {
        this.loginData.active = false
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style>
</style>
