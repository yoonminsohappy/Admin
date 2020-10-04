import Vue from 'vue'
import Vuex from 'vuex'
import order from './modules/order'

Vue.use(Vuex); // vuex를 전역으로 사용할수 있음

export const store = new Vuex.Store({
      modules: {
        order
      }
}); 