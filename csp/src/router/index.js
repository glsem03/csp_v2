import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage'
import MainPage from "../views/MainPage"
import SchedulePage from "../views/SchedulePage"
import TeachersPage from "../views/TeachersPage"

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/main',
    name: 'Main',
    component: MainPage
  },
  {
    path: '/schedule',
    name: 'Schedule',
    component: SchedulePage
  },
  {
    path: '/teachers',
    name: 'Teachers',
    component: TeachersPage
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
