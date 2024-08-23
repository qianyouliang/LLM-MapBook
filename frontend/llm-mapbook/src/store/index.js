import Vue from "vue";
import Vuex from 'vuex';
// 引入模块
import user from "./modules/user";
import map from "./modules/map";

Vue.use(Vuex);

const store = new Vuex.Store({
    state:{

    },
    mutations:{

    },
    getters:{

    },
    actions:{

    },
    modules:{
        map,
        user,
    }
});

export default store;