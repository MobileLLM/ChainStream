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
                path: 'Agents',
                name: 'Agent',
                component: () => import('@/components/view/monitor/agents.vue')
            },
            {
                path: 'Streams',
                name: 'Stream',
                component: () => import('@/components/view/monitor/streams.vue')
            },

        ]

    },
    {
        path: '/memory',
        name: 'Memory',
        children: [
            {
                path: 'Memory',
                name: 'Memory',
                component: () => import('@/components/view/memory/memory.vue')
            }
        ]
    },
    {
        path: '/analysis',
        name: 'Analysis',
        children: [
            {
                path: 'Analysis',
                name: 'Analysis',
                component: () => import('@/components/view/analysis/analysis.vue')
            }
        ]
    },
    {
        path: '/device',
        name: 'Device',
        children: [
            {
                path: 'Device',
                name: 'Device',
                component: () => import('@/components/view/devices/devices.vue')
            }
        ]
    },
    {
        path: '/tools',
        name: 'Tools',
        children: [
            {
                path: 'Tools',
                name: 'Tools',
                component: () => import('@/components/view/tools/tools.vue')
            },
            {
                path: 'LLMs',
                name: 'LLMs',
                component: () => import('@/components/view/tools/llms.vue')
            }
        ]
    },
    {
        path: '/store',
        name: 'Store',
        children: [
            {
                path: 'Store',
                name: 'Store',
                component: () => import('@/components/view/store/store.vue')
            },
        ]
    },
    {
        path: '/generator',
        name: 'AgentGenerator',
        children: [
            {
                path: 'Generator',
                name: 'AgentGenerator',
                component: () => import('@/components/view/generator/generator.vue')
            },
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