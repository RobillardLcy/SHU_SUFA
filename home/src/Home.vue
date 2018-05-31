<template>
  <div id="home">
    <v-app>
      <v-navigation-drawer fixed :clipped="$vuetify.breakpoint.width > 1264" app v-model="drawer">
        <v-list>
          <v-list-tile router to="/home">
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>主页</v-list-tile-content>
          </v-list-tile>
          <v-list-group
            v-model="item.active"
            v-for="item in items"
            :prepend-icon="item.action"
            :key="item.title"
            no-action>
            <v-list-tile slot="activator" router :to="item.url">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
              v-for="subItem in item.items"
              :key="subItem.title"
              :prepend-icon="subItem.action"
              router
              :to="subItem.url">
                <v-list-tile-content>
                  <v-list-tile-title>{{ subItem.title }}</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
          <v-list-tile router to="/activities">
            <v-list-tile-action>
              <v-icon>
                local_activity
              </v-icon>
            </v-list-tile-action>
            <v-list-tile-content>活动</v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-divider v-show="college.id"></v-divider>
        <v-subheader v-show="college.id">我的球队</v-subheader>
        <v-list>
          <v-list-tile v-show="college.id" router :to="college.url">
            <v-list-tile-avatar>
              <img :src="college.logo">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ college.name }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
          <v-list-tile v-show="team.id" router :to="team.url">
            <v-list-tile-avatar>
              <img :src="team.logo">
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ team.name }}</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
        <v-divider></v-divider>
        <v-subheader v-show="studentID">报名通道</v-subheader>
        <v-list>
          <v-list-tile
            v-for="activity in activities"
            :key="activity.title"
            router
            :to="activity.url">
            <v-list-tile-content>
              <v-list-tile-title>{{ activity.name }}</v-list-tile-title>
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
        <v-menu v-show="studentID" v-model="menu">
          <v-btn color="orange" dark slot="activator">
            <v-icon left>account_circle</v-icon>
            {{ studentID }}
          </v-btn>
          <v-card>
            <v-list>
              <v-list-tile>
                <v-btn flat small color="primary" to="/member">个人中心</v-btn>
              </v-list-tile>
              <v-list-tile>
                <v-btn flat small color="primary" to="/team">我的球队</v-btn>
              </v-list-tile>
              <v-list-tile>
                <v-btn flat small color="red" @click="logout">注销</v-btn>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-menu>
        <v-dialog v-show="!studentID" v-model="loginDialog" max-width=800>
          <v-btn color="success" dark slot="activator">
            登录
          </v-btn>
          <login-dialog :loginDialog="loginDialog" @closeLoginDialog="loginDialog = false" @loginSuccess="updateInfo"></login-dialog>
        </v-dialog>
        <v-btn color="success" dark v-show="!studentID && $vuetify.breakpoint.width > 1264" router :to="register">
          社团注册
        </v-btn>
      </v-toolbar>
      <v-content>
        <v-container fluid>
          <router-view :studentID="studentID"></router-view>
        </v-container>
      </v-content>
      <v-footer app>
        <v-spacer></v-spacer>
        <div class="text-xs-center">
          © 2017-{{ new Date().getFullYear() }} <a href="https://www.shusufa.com">上海大学足球协会</a><br/>社团所属学校：<a href="http://www.shu.edu.cn">上海大学</a>
        </div>
        <v-spacer></v-spacer>
      </v-footer>
    </v-app>
  </div>
</template>

<script>
import Login from '@/components/member/Login'
export default {
  name: 'home',
  data: () => ({
    drawer: false,
    loginDialog: false,
    menu: false,
    register: '/register',
    studentID: '',
    // TODO: 网站导航栏可管理，即网站导航栏由后台数据库导入
    items: [
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
          { title: '上海大学男子足球队', url: '/team/man-team' },
          { title: '上海大学女子足球队', url: '/team/woman-team' },
          { title: '学院队伍', url: '/team/college-team' },
          { title: '年级梯队', url: '/team/grade-team' },
          { title: '自由队伍', url: '/team/free-team' }
        ]
      },
      {
        action: 'whatshot',
        title: '比赛',
        items: [
          { title: '上海大学学院杯', url: '/league/college-cup' },
          { title: '上海大学足球协会杯', url: '/league/association-cup' },
          { title: '上海大学足球协会新生杯', url: '/league/newStudent-cup' },
          { title: '自由组织赛事', url: '/league/free-league' }
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
      }
    ],
    // TODO: 活动从数据库中读取，动态更新
    activities: [
    ],
    college: {
    },
    team: {
    }
  }),
  props: {
  },
  components: {
    'login-dialog': Login
  },
  computed: {
  },
  updated: function () {
    if (this.$cookie.get('id')) {
      this.redirectLogin()
    }
  },
  methods: {
    redirectLogin: function () {
      this.studentID = this.$cookie.get('id')
      this.updateInfo()
      if (window.location.hash === '#/login') {
        this.$router.push('/')
      }
    },
    // 账户注销
    logout: function () {
      this.$axios.get('member/logout/')
        .then(response => {
          this.$cookie.delete('id')
          this.$cookie.delete('mobile')
          window.sessionStorage.removeItem('auth')
          this.college = {}
          this.team = {}
          this.studentID = null
        })
        .catch(error => {
          console.log(error)
          this.$cookie.delete('id')
          this.$cookie.delete('mobile')
          window.sessionStorage.removeItem('auth')
          this.college = {}
          this.team = {}
          this.studentID = null
        })
    },
    updateInfo: function () {
      let collegeInfo = JSON.parse(window.localStorage.getItem('college'))
      if (collegeInfo) {
        this.college.id = collegeInfo.id
        this.college.name = collegeInfo.name
        this.college.logo = collegeInfo.logo
        this.college.url = '/team/college-team/' + collegeInfo.id
      }
      let teamInfo = JSON.parse(window.localStorage.getItem('team'))
      if (teamInfo) {
        this.team.id = teamInfo.id
        this.team.name = teamInfo.name
        this.team.logo = teamInfo.logo
        this.team.url = '/team/free-team/' + teamInfo.id
      }
    }
  }
}
</script>

<style>
</style>
