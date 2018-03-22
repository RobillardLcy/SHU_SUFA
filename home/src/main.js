// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import Axios from 'axios'
import Home from './Home'
import router from './router'

// TODO: set false
Vue.config.productionTip = true

Vue.use(Vuetify)
import('../node_modules/vuetify/dist/vuetify.min.css')

Vue.prototype.$axios = Axios.create({
  baseURL: 'http://www.yellowsea.top/api/',
  timeout: 5000,
  headers: {'Content-Type': 'application/json;Charset=utf-8'},
  withCredentials: true
})

/* eslint-disable no-new */
new Vue({
  el: '#home',
  router,
  template: '<Home/>',
  components: { Home }
})
