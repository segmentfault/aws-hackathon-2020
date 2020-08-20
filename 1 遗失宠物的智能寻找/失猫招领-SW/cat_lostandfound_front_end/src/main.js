import Vue from 'vue'
import App from './App.vue'
import router from './router.js'
import request from './fetch.js'

import Vant from 'vant'
import 'vant/lib/index.css'

Vue.config.productionTip = false
Vue.prototype.$request = request
Vue.prototype.$imgServer = 'https://fzhcats.s3.ap-northeast-1.amazonaws.com/'

Vue.use(Vant)
Vue.prototype.$toast.setDefaultOptions('loading', {
  forbidClick: true,
  duration: 0,
})
// Vue.use(Lazyload, {
//   lazyComponent: true,
// })

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app')
