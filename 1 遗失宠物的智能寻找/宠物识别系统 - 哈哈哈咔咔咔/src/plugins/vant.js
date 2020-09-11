// 按需全局引入 vant组件
import Vue from 'vue'
import {
  Button,
  List,
  Cell,
  Tabbar,
  TabbarItem,
  Grid,
  GridItem,
  Image as VanImage,
  Uploader,
  Toast,
  Dialog
} from 'vant'

Vue.use(Button)
Vue.use(Cell)
Vue.use(List)
Vue.use(Tabbar).use(TabbarItem)
Vue.use(Grid).use(GridItem);
Vue.use(VanImage)
Vue.use(Uploader);
Vue.use(Dialog);
Vue.use(Toast);
