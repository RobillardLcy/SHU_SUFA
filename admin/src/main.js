// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import axios from 'axios'
import Admin from './Admin'
import router from './router'

// TODO: set false
Vue.config.productionTip = true

Vue.use(Vuetify)
import('../node_modules/vuetify/dist/vuetify.min.css')
import('../node_modules/material-icons/iconfont/material-icons.css')

Vue.prototype.$axios = axios.create({
  baseURL: 'http://admin.yellowsea.top:8000/api/'
  // baseURL: 'https://admin.shusufa.com/api/'
})

/* eslint-disable no-new */
new Vue({
  el: '#admin',
  router,
  template: '<Admin/>',
  components: { Admin }
})
