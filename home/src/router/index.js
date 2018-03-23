import Vue from 'vue'
import Router from 'vue-router'

import NotFoundPage from '@/components/NotFoundPage'
import Home from '@/components/Home'

import Member from '@/components/member/Member'
import Login from '@/components/member/Login'
import Register from '@/components/member/Register'

import About from '@/components/about/About'
import Community from '@/components/about/Community'
import Teacher from '@/components/about/Teacher'
import President from '@/components/about/President'
import Affair from '@/components/about/Affair'
import Publicity from '@/components/about/Publicity'
import Liaison from '@/components/about/Liaison'
import Finance from '@/components/about/Finance'
import Technology from '@/components/about/Technology'
import Referee from '@/components/about/Referee'
import Manager from '@/components/about/Manager'

import Team from '@/components/team/Team'
import ManTeam from '@/components/team/ManTeam'
import WomanTeam from '@/components/team/WomanTeam'
import GradeTeam from '@/components/team/GradeTeam'
import FreeTeam from '@/components/team/FreeTeam'

import Leagues from '@/components/leagues/Leagues'
import CollegeCup from '@/components/leagues/CollegeCup'
import AssociationCup from '@/components/leagues/AssociationCup'
import NewStudentCup from '@/components/leagues/NewStudentCup'
import FreeLeagues from '@/components/leagues/FreeLeagues'

import FanClub from '@/components/fanClub/FanClub'

import ActivitiesList from '@/components/activities/ActivitiesList'
import Activity from '@/components/activities/Activity'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      meta: {
        need_log: false
      }
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
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        need_log: false
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: {
        need_log: false
      }
    },
    {
      path: '/member',
      name: 'Member',
      component: Member,
      meta: {
        need_log: true
      }
    },
    {
      path: '/about',
      name: 'About',
      component: About,
      children: [
        {
          path: 'community',
          name: 'Community',
          components: {
            content: Community
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'teacher',
          name: 'Teacher',
          components: {
            content: Teacher
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'president',
          name: 'President',
          components: {
            content: President
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'affair',
          name: 'Affair',
          components: {
            content: Affair
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'publicity',
          name: 'Publicity',
          components: {
            content: Publicity
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'liaison',
          name: 'Liaison',
          components: {
            content: Liaison
          }
        },
        {
          path: 'finance',
          name: 'Finance',
          components: {
            content: Finance
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'technology',
          name: 'Technology',
          components: {
            content: Technology
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'referee',
          name: 'Referee',
          components: {
            content: Referee
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'manager',
          name: 'Manager',
          components: {
            content: Manager
          },
          meta: {
            need_log: false
          }
        }
      ]
    },
    {
      path: '/team',
      name: 'Team',
      component: Team,
      children: [
        {
          path: 'man_team',
          name: 'ManTeam',
          components: {
            team: ManTeam
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'woman_team',
          name: 'WomanTeam',
          components: {
            team: WomanTeam
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'grade_team',
          name: 'GradeTeam',
          components: {
            team: GradeTeam
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'free_team',
          name: 'FreeTeam',
          components: {
            team: FreeTeam
          },
          meta: {
            need_log: true
          }
        }
        // TODO: 添加队伍页面，便于队伍管理及报名
      ]
    },
    {
      path: '/leagues',
      name: 'Leagues',
      component: Leagues,
      children: [
        {
          path: 'college_cup',
          name: 'CollegeCup',
          components: {
            league: CollegeCup
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'association_cup',
          name: 'AssociationCup',
          components: {
            league: AssociationCup
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'newStudent_cup',
          name: 'NewStudentCup',
          components: {
            league: NewStudentCup
          },
          meta: {
            need_log: false
          }
        },
        {
          path: 'free_leagues',
          name: 'FreeLeagues',
          components: {
            league: FreeLeagues
          },
          meta: {
            need_log: true
          }
        }
      ]
    },
    {
      path: '/fanClub/:club',
      name: 'FanClub',
      component: FanClub,
      meta: {
        need_log: false
      }
    },
    {
      path: '/activities',
      name: 'ActivitiesList',
      component: ActivitiesList,
      meta: {
        need_log: false
      }
    },
    {
      path: '/activity/:activity',
      name: 'Activity',
      component: Activity,
      meta: {
        need_log: true
      }
    }
  ]
})

// TODO: 路由判断是否需要登录
router.beforeEach((to, from, next) => {
  if (window.sessionStorage.getItem('id') === null) {
    if (to.meta.need_log) {
      if (to.path !== '/login') {
        next('/login')
      }
    }
  }
  next()
})

export default router
