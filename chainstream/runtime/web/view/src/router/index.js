// import Vue from 'vue'
// import { createApp } from 'vue'
// import VueRouter from 'vue-router'
// import Router from 'vue-router'
import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../components/Home.vue'
// import App from '../App.vue'
// import * as Vue from "echarts";


// Vue.use(VueRouter);
// Vue.use(Router)

const routes= [
    {
        path: '/',
        redirect: '/home'
    },
    {
        path: '',
        redirect: '/home'
    },
    {
        path: '/monitor',
        name: 'Monitor',
        children: [
            {
                path: 'StreamGraph',
                name: 'StreamGraph',
                component: () => import('@/components/view/monitor/StreamGraph.vue')
            },
            {
                path: 'Agent',
                name: 'Agent',
                component: () => import('@/components/view/monitor/agents.vue')
            }
        ]

    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../components/NotFound.vue')
    }

];

// const router =  new VueRouter({
//     mode: 'history',
//     routes: routes
// });

export default new createRouter({
    mode: 'history',
    history: createWebHashHistory(),
    routes: routes
})

// export default router;
// createApp(App).use(router)
// export default new Router({
//     mode: 'history',
//     routes: routes
// })