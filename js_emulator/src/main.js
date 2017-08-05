import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VueWamp from 'vue-wamp'
import VueCookies from 'vue-cookies'
import Home from './Home.vue'

Vue.use(VueWamp, {
  debug: true,
  lazy_open: false,
  url: 'ws://api.swadge.com:1337/ws',
  realm: 'swadges',
  onopen: function(session, details) {
    session.authid = "simulator";
    session.onchallenge = function(sess, method, extra) {
        return "icantbelieveitsnotabadge";
    }
    console.log('WAMP connected', session, details);
  },
  onclose: function(reason, details) {
    console.log('WAMP closed: ' + reason, details);
  }
});

Vue.use(VueRouter);

Vue.use(VueCookies);

const routes = [{
    path: '/',
    component: Home
  }
];

const router = new VueRouter({
  routes
});

const store = new Vuex.Store();

window.eventHub = new Vue();

window.addEventListener('keydown', function(event) {
      if (event.repeat) return;
      if (event.keyCode == 38 || event.keyCode == 104) {
        // UP
        eventHub.$emit('key_press', 'up');
      } else if (event.keyCode == 40 || event.keyCode == 98) {
        // DOWN
        eventHub.$emit('key_press', 'down');
      } else if (event.keyCode == 37 || event.keyCode == 100) {
        // LEFT
        eventHub.$emit('key_press', 'left');
      } else if (event.keyCode == 39 || event.keyCode == 102) {
        // RIGHT
        eventHub.$emit('key_press', 'right');
      } else if (event.keyCode == 65) {
        // A
        eventHub.$emit('key_press', 'a');
      } else if (event.keyCode == 66) {
        // B
        eventHub.$emit('key_press', 'b');
      } else if (event.keyCode == 13) {
        // Select (Enter)
        eventHub.$emit('key_press', 'select');
      } else if (event.keyCode == 8) {
        // Start (Backspace)
        eventHub.$emit('key_press', 'start');
      }
    });

window.addEventListener('keyup', function(event) {
      if (event.keyCode == 38 || event.keyCode == 104) {
        // UP
        eventHub.$emit('key_release', 'up');
      } else if (event.keyCode == 40 || event.keyCode == 98) {
        // DOWN
        eventHub.$emit('key_release', 'down');
      } else if (event.keyCode == 37 || event.keyCode == 100) {
        // LEFT
        eventHub.$emit('key_release', 'left');
      } else if (event.keyCode == 39 || event.keyCode == 102) {
        // RIGHT
        eventHub.$emit('key_release', 'right');
      } else if (event.keyCode == 65) {
        // A
        eventHub.$emit('key_release', 'a');
      } else if (event.keyCode == 66) {
        // B
        eventHub.$emit('key_release', 'b');
      } else if (event.keyCode == 13) {
        // Select (Enter)
        eventHub.$emit('key_release', 'select');
      } else if (event.keyCode == 8) {
        // Start (Backspace)
        eventHub.$emit('key_release', 'start');
      }
    });

window.vue = new Vue({
  router,
  store,
  el: '#app',
  render: h => h(Home)
})
