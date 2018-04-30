import Vue from 'vue'
import Router from 'vue-router'
import vueCookie from 'vue-cookie'
import Dashboard from '@/components/Dashboard'

import NotFoundPage from '@/components/public/NotFoundPage'
import Login from '@/components/public/Login'

import Community from '@/components/community/Community'
import Departments from '@/components/community/Departments'
import Admins from '@/components/community/Admins'
import Members from '@/components/community/Members'

import News from '@/components/news/News'
import NewsList from '@/components/news/NewsList'
import NewsForum from '@/components/news/NewsForum'
import NewsEditor from '@/components/news/NewsEditor'

import Teams from '@/components/teams/Teams'
import ManTeam from '@/components/teams/ManTeam'
import WomanTeam from '@/components/teams/WomanTeam'
import GradeTeam from '@/components/teams/GradeTeam'
import FreeTeam from '@/components/teams/FreeTeam'

import Leagues from '@/components/leagues/Leagues'
import LeaguesList from '@/components/leagues/LeaguesList'
import LeaguesCalendar from '@/components/leagues/LeaguesCalendar'
import LeaguesData from '@/components/leagues/LeaguesData'
import LeagueSignup from '@/components/leagues/LeagueSignup'

import Activities from '@/components/activities/Activities'
import ActivitiesList from '@/components/activities/ActivitiesList'
import ActivitiesCalendar from '@/components/activities/ActivitiesCalendar'
import ActivitySignup from '@/components/activities/ActivitySignup'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/404',
      name: '404',
      component: NotFoundPage,
      meta: {
        need_log: false
      }
    },
    {
      path: '*',
      redirect: '/404'
    },
    {
      path: '/community',
      name: 'Community',
      component: Community,
      children: [
        {
          path: 'departments',
          name: 'Departments',
          component: Departments
        },
        {
          path: 'admins',
          name: 'Admins',
          component: Admins
        },
        {
          path: 'members',
          name: 'Members',
          component: Members
        }
      ]
    },
    {
      path: '/news',
      name: 'News',
      component: News,
      children: [
        {
          path: 'list',
          name: 'NewsList',
          component: NewsList
        },
        {
          path: 'forum',
          name: 'NewsForum',
          component: NewsForum
        },
        {
          path: 'editor',
          name: 'NewsEditor',
          component: NewsEditor
        }
      ]
    },
    {
      path: '/teams',
      name: 'Teams',
      component: Teams,
      children: [
        {
          path: 'man_team',
          name: 'ManTeam',
          component: ManTeam
        },
        {
          path: 'woman_team',
          name: 'WomanTeam',
          component: WomanTeam
        },
        {
          path: 'grade_team',
          name: 'GradeTeam',
          component: GradeTeam
        },
        {
          path: 'free_team',
          name: 'FreeTeam',
          component: FreeTeam
        }
      ]
    },
    {
      path: '/leagues',
      name: 'Leagues',
      component: Leagues,
      children: [
        {
          path: 'list',
          name: 'LeaguesList',
          component: LeaguesList
        },
        {
          path: 'calendar',
          name: 'LeaguesCalendar',
          component: LeaguesCalendar
        },
        {
          path: 'data',
          name: 'LeaguesData',
          component: LeaguesData
        },
        {
          path: 'signup',
          name: 'LeagueSignup',
          component: LeagueSignup
        }
      ]
    },
    {
      path: '/activities',
      name: 'Activities',
      component: Activities,
      children: [
        {
          path: 'list',
          name: 'ActivitiesList',
          component: ActivitiesList
        },
        {
          path: 'calendar',
          name: 'ActivitiesCalendar',
          component: ActivitiesCalendar
        },
        {
          path: 'signup',
          name: 'ActivitySignup',
          component: ActivitySignup
        }
      ]
    }
  ]
})

// TODO: 验证是否登录
router.beforeEach((to, from, next) => {
  if (vueCookie.get('id') && vueCookie.get('admin')) {
    next()
  } else {
    if (to.path !== '/login') {
      next('/login')
    } else {
      next()
    }
  }
})

export default router
