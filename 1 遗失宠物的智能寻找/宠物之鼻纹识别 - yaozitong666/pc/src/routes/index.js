import loadable from '@/utils/loadable'

const Index = loadable(() => import(/* webpackChunkName: 'index' */ '@/views/Index'))

// 通用
const ButtonView = loadable(() => import(/* webpackChunkName: 'button' */ '@/views/PublicView/Button'))

// 导航
const DropdownView = loadable(() => import(/* webpackChunkName: 'dropdown' */ '@/views/NavView/Dropdown'))
const MenuView = loadable(() => import(/* webpackChunkName: 'menu' */ '@/views/NavView/Menu'))
const StepView = loadable(() => import(/* webpackChunkName: 'step' */ '@/views/NavView/Step'))

// 表单
// 其它
const ProgressView = loadable(() => import(/* webpackChunkName: 'progress' */ '@/views/Others/Progress'))
const AnimationView = loadable(() => import(/* webpackChunkName: 'animation' */ '@/views/Others/Animation'))
const EditorView = loadable(() => import(/* webpackChunkName: 'editor' */ '@/views/Others/Editor'))
const UploadView = loadable(() => import(/* webpackChunkName: 'upload' */ '@/views/Others/Upload'))

const About = loadable(() => import(/* webpackChunkName: 'about' */ '@/views/About'))

const routes = [
  {path: '/index', exact: true, name: 'Index', component: Index, auth: [1]},
  {path: '/public/button', exact: false, name: '识别', component: ButtonView, auth: [1]},
  {path: '/nav/dropdown', exact: false, name: '下拉菜单', component: DropdownView},
  {path: '/nav/menu', exact: false, name: '下拉菜单', component: MenuView},
  {path: '/nav/steps', exact: false, name: '步骤条', component: StepView},
  {path: '/others/progress', exact: false, name: '进度条', component: ProgressView, auth: [1]},
  {path: '/others/animation', exact: false, name: '动画', component: AnimationView, auth: [1]},
  {path: '/others/editor', exact: false, name: '富文本', component: EditorView, auth: [1]},
  {path: '/others/upload', exact: false, name: '上传', component: UploadView, auth: [1]},
  {path: '/about', exact: false, name: '关于', component: About, auth: [1]}
]

export default routes
