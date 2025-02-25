import Vue from 'vue';
import Router from 'vue-router';
import UserAuth from '@/components/UserAuth.vue';
import LostItemRegister from '@/components/LostItemRegister.vue';
import FoundItemRegister from '@/components/FoundItemRegister.vue';
import ItemList from '@/components/ItemList.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'UserAuth',
      component: UserAuth
    },
    {
      path: '/lost-item-register',
      name: 'LostItemRegister',
      component: LostItemRegister
    },
    {
      path: '/found-item-register',
      name: 'FoundItemRegister',
      component: FoundItemRegister
    },
    {
      path: '/item-list',
      name: 'ItemList',
      component: ItemList
    }
  ]
});