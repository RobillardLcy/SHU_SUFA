// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import axios from 'axios'
import vueCookie from 'vue-cookie'
import Admin from './Admin'
import router from './router'

// TODO: set false
Vue.config.productionTip = true

Vue.use(Vuetify)
import('../node_modules/vuetify/dist/vuetify.min.css')
import('../node_modules/material-design-icons-iconfont/dist/material-design-icons.css')

Vue.prototype.$axios = axios.create({
  baseURL: 'http://administrator.shusufa.com/api/',
  timeout: 5000,
  headers: {'Content-Type': 'application/json;Charset=utf-8'},
  withCredentials: true
})

Vue.prototype.$cookie = vueCookie

/* eslint-disable no-new */
new Vue({
  el: '#admin',
  router,
  template: '<Admin/>',
  components: { Admin }
})
