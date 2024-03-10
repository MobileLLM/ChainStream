import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../components/Home.vue'
import App from '../App.vue'


Vue.use(Router);

const routes= [
    {
        path: '',
        name: 'Home',
        component: App
    },

];

export default new VueRouter({
    mode: 'history',
    routes: routes
});