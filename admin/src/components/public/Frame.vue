<template>
  <div class="Frame">
    <v-app>
      <v-navigation-drawer fixed :clipped="$vuetify.breakpoint.width > 1264" app v-model="drawer">
        <v-list dense>
          <v-list-tile router to="/">
            <v-list-tile-action>
              <v-icon>dashboard</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>控制面板</v-list-tile-content>
          </v-list-tile>
          <v-list-group
            v-for="item in items"
            :value="item.active"
            :key="item.title"
            :prepend-icon="item.action"
            no-action>
            <v-list-tile slot="activator" router :to="item.url">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile v-for="subItem in item.items" :key="subItem.title" :prepend-icon="subItem.icon" router :to="subItem.url">
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
          <v-btn color="orange" dark slot="activator">
            <v-icon left>account_circle</v-icon>
            {{ studentID }}
          </v-btn>
          <v-card>
            <v-list>
              <v-list-tile>
                <v-btn flat small color="red" @click="logOut">注销</v-btn>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-menu>
      </v-toolbar>
      <v-content>
        <v-container>
          <router-view name="content"/>
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
export default {
  name: 'Frame',
  data: () => ({
    drawer: null,
    menu: false,
    departments: [],
    studentID: '15121600',
    items: [
      {
        action: 'account_balance',
        title: '社团管理',
        items: [
          { title: '部门管理', url: '/community/departments' },
          { title: '社团骨干', url: '/community/administrator' },
          { title: '社团成员', url: '/community/member' }
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
          { title: '男子足球队', url: '/team/man_team' },
          { title: '女子足球队', url: '/team/woman_team' },
          { title: '年级梯队', url: '/team/grade_team' },
          { title: '自由队伍', url: '/team/free_team' }
        ]
      },
      {
        action: 'whatshot',
        title: '赛事管理',
        items: [
          { title: '赛事信息', url: '/league/list' },
          { title: '赛事赛程', url: '/league/calendar' },
          { title: '赛事数据', url: '/league/data' },
          { title: '赛事报名', url: '/league/signup' }
        ]
      },
      {
        action: 'assistant_photo',
        title: '活动管理',
        items: [
          { title: '活动信息', url: '/activity/list' },
          { title: '活动日历', url: '/activity/calendar' },
          { title: '活动报名', url: '/activity/signup' }
        ]
      }
    ]
  }),
  props: {

  },
  mounted: () => {
  },
  updated: function () {
    this.studentID = this.$cookie.get('id')
  },
  computed: {
  },
  methods: {
    logOut: function () {
      // 注销
      this.$axios.post('logout/')
        .then(response => {
          this.$cookie.delete('id')
          this.$cookie.delete('admin')
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
