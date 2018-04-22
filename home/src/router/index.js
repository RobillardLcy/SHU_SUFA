import Vue from 'vue'
import Router from 'vue-router'
import vueCookie from 'vue-cookie'

import NotFoundPage from '@/components/public/NotFoundPage'
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
import CollegeTeam from '@/components/team/CollegeTeam'
import CollegeTeamProfile from '@/components/team/CollegeTeamProfile'
import GradeTeam from '@/components/team/GradeTeam'
import FreeTeam from '@/components/team/FreeTeam'
import FreeTeamProfile from '@/components/team/FreeTeamProfile'

import Leagues from '@/components/leagues/Leagues'
import CollegeCup from '@/components/leagues/CollegeCup'
import AssociationCup from '@/components/leagues/AssociationCup'
import NewStudentCup from '@/components/leagues/NewStudentCup'
import FreeLeagues from '@/components/leagues/FreeLeagues'
import FreeLeaguesProfile from '@/components/leagues/FreeLeaguesProfile'

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
      component: Home
    },
    {
      path: '/404',
      name: '404',
      component: NotFoundPage
    },
    {
      path: '*',
      redirect: '/404'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/member',
      name: 'Member',
      component: Member
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
          }
        },
        {
          path: 'teacher',
          name: 'Teacher',
          components: {
            content: Teacher
          }
        },
        {
          path: 'president',
          name: 'President',
          components: {
            content: President
          }
        },
        {
          path: 'affair',
          name: 'Affair',
          components: {
            content: Affair
          }
        },
        {
          path: 'publicity',
          name: 'Publicity',
          components: {
            content: Publicity
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
          }
        },
        {
          path: 'technology',
          name: 'Technology',
          components: {
            content: Technology
          }
        },
        {
          path: 'referee',
          name: 'Referee',
          components: {
            content: Referee
          }
        },
        {
          path: 'manager',
          name: 'Manager',
          components: {
            content: Manager
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
          path: 'man-team',
          name: 'ManTeam',
          components: {
            team: ManTeam
          }
        },
        {
          path: 'woman-team',
          name: 'WomanTeam',
          components: {
            team: WomanTeam
          }
        },
        {
          path: 'college-team',
          name: 'CollegeTeam',
          components: {
            team: CollegeTeam
          }
        },
        {
          path: 'college-team/:college_id',
          name: 'CollegeTeamProfile',
          props: true,
          components: {
            team: CollegeTeamProfile
          }
        },
        {
          path: 'grade-team',
          name: 'GradeTeam',
          components: {
            team: GradeTeam
          }
        },
        {
          path: 'free-team',
          name: 'FreeTeam',
          components: {
            team: FreeTeam
          }
        },
        {
          path: 'free-team/:team-id',
          name: 'FreeTeamProfile',
          components: {
            team: FreeTeamProfile
          }
        }
      ]
    },
    {
      path: '/leagues',
      name: 'Leagues',
      component: Leagues,
      children: [
        {
          path: 'college-cup',
          name: 'CollegeCup',
          components: {
            league: CollegeCup
          }
        },
        {
          path: 'association-cup',
          name: 'AssociationCup',
          components: {
            league: AssociationCup
          }
        },
        {
          path: 'newStudent-cup',
          name: 'NewStudentCup',
          components: {
            league: NewStudentCup
          }
        },
        {
          path: 'free-leagues',
          name: 'FreeLeagues',
          components: {
            league: FreeLeagues
          }
        },
        {
          path: 'free-leagues/:leagues-id',
          name: 'FreeLeaguesProfile',
          components: {
            league: FreeLeaguesProfile
          }
        }
      ]
    },
    {
      path: '/fanClub/:club',
      name: 'FanClub',
      component: FanClub
    },
    {
      path: '/activities',
      name: 'ActivitiesList',
      component: ActivitiesList
    },
    {
      path: '/activity/:activity',
      name: 'Activity',
      component: Activity
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (!vueCookie.get('id')) {
    if (to.meta.need_log) {
      next('/login')
    } else {
      next()
    }
  } else if (to.path === '/login') {
    next('/')
  } else {
    next()
  }
})

export default router
