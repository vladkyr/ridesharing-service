import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("../views/Home.vue")
    },
    {
        path: "/init-db",
        name: "initDB",
        component: () => import("../views/InitDB.vue")
    },
    {
        path: "/book-ride",
        name: "bookRide",
        component: () => import("../views/BookRide.vue"),
        props: (route) => ({ database: route.query.database })
    },
    {
        path: "/report",
        name: "report",
        component: () => import("../views/Report.vue"),
        props: (route) => ({ database: route.query.database })
    },
    {
        path: "/migrate",
        name: "migrate",
        component: () => import("../views/Migrate.vue")
    }
];

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes
});

export default router;
