<template>
  <div id="admin">
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
          <v-list-tile href="http://www.shusufa.com">
            <v-list-tile-action>
              <v-icon>home</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>回到网站首页</v-list-tile-title>
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
        <v-menu offset-x :nudge-width="150" v-model="menu">
          <v-btn color="light-blue darken-4" dark slot="activator">
            <v-icon left>account_circle</v-icon>
            {{ adminProfile.studentName }}
          </v-btn>
          <v-card>
            <v-list>
              <v-list-tile avatar>
                <v-list-tile-avatar>
                  <img :src="adminProfile.photo">
                </v-list-tile-avatar>
                <v-list-tile-content>
                  <v-list-tile-title>{{ adminProfile.studentID }} {{ adminProfile.studentName }}</v-list-tile-title>
                  <v-list-tile-sub-title>{{ adminProfile.position }} {{ adminProfile.department }}</v-list-tile-sub-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
            <v-divider></v-divider>
            <v-list>
              <v-card-actions>
                <v-btn flat small color="primary" to="/">个人中心</v-btn>
                <v-spacer></v-spacer>
                <v-btn flat small color="red" @click="logOut">注销</v-btn>
              </v-card-actions>
            </v-list>
          </v-card>
        </v-menu>
      </v-toolbar>
      <v-content>
        <v-container>
          <router-view/>
        </v-container>
      </v-content>
      <v-footer app>
        <v-spacer></v-spacer>
        <div class="text-xs-center">
          © 2017-{{ new Date().getFullYear() }} <a href="https://www.shusufa.com">上海大学足球协会</a>&nbsp;&nbsp;&nbsp;&nbsp;社团所属学校：<a href="http://www.shu.edu.cn">上海大学</a>
        </div>
        <v-spacer></v-spacer>
      </v-footer>
    </v-app>
  </div>
</template>

<script>

export default {
  name: 'admin',
  data: () => ({
    drawer: null,
    login: true,
    menu: false,
    departments: [],
    adminProfile: {
      studentID: '15121600',
      studentName: '黄海',
      position: '主席',
      department: '主席团',
      photo: '/static/logo/sufa_logo.png'
    },
    items: [
      {
        action: 'dashboard',
        title: '控制面板',
        url: '/'
      },
      {
        action: 'account_balance',
        title: '社团管理',
        items: [
          { title: '部门管理', url: '/community/departments' },
          { title: '社团骨干', url: '/community/admins' },
          { title: '社团成员', url: '/community/members' }
        ]
      },
      {
        action: 'library_books',
        title: '新闻管理',
        items: [
          { title: '新闻列表', url: '/news/list' },
          { title: '新闻板块', url: '/news/forum' },
          { title: '新闻编辑', url: '/news/editor' }
        ]
      },
      {
        action: 'group',
        title: '队伍管理',
        items: [
          { title: '男子足球队', url: '/teams/man_team' },
          { title: '女子足球队', url: '/teams/woman_team' },
          { title: '年级梯队', url: '/teams/grade_team' },
          { title: '自由队伍', url: '/teams/free_team' }
        ]
      },
      {
        action: 'whatshot',
        title: '赛事管理',
        items: [
          { title: '赛事信息', url: '/leagues/list' },
          { title: '赛事赛程', url: '/leagues/calendar' },
          { title: '赛事数据', url: '/leagues/data' },
          { title: '赛事报名', url: '/leagues/signup' }
        ]
      },
      {
        action: 'assistant_photo',
        title: '活动管理',
        items: [
          { title: '活动信息', url: '/activities/list' },
          { title: '活动日历', url: '/activities/calendar' },
          { title: '活动报名', url: '/activities/signup' }
        ]
      }
    ]
  }),
  props: {

  },
  computed: {

  },
  methods: {
    logOut: function () {
      this.login.active = false
    }
  }
}
</script>

<style>
</style>
