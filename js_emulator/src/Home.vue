<template>
  <div id="swadge-1" class="swadge">
    <span class="swadge-mac">{{ mac }}</span>
    <div class="swadge-lights">
      <div v-for="light in lights" class="light" :style="'background-color: rgb(' + light.r + ',' + light.g + ',' + light.b + ');'"></div>
    </div>
    <span v-if="show_screen" class="swadge-screen-text">{{ text }}</span>
    <br/>
    <div class="swadge-buttons">
      <button v-for="button in buttons" v-on:mouseup="onButtonUp(button.id)" v-on:mousedown="onButton(button.id)" :class="'btn-' + button.id" :data-key="button.id"><img v-if="button.img" :src="button.img"/>{{ button.label }}</button>
    </div>
    <div class="swadge-controls">
    <label><input type="checkbox" v-model="show_screen"/>Show Screen</label>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        buttons: [
            {id: 'up', img: 'assets/triangle-up.svg'},
            {id: 'left', img: 'assets/triangle-left.svg'},
            {id: 'right', img: 'assets/triangle-right.svg'},
            {id: 'down', img: 'assets/triangle-down.svg'},
            {id: 'b', label: 'B'},
            {id: 'a', label: 'A'},
            {id: 'select', label: 'Select'},
            {id: 'start', label: 'Start'}],
        lights: [{r: 128, g: 192, b: 255},
                 {r: 128, g: 192, b: 255},
                 {r: 128, g: 192, b: 255},
                 {r: 128, g: 192, b: 255}],
        mac: Math.floor(Math.random() * (0xffffffffffff - 0x010000000000) + 0x010000000000),
        text: '',
        show_screen: false,
        update_id: 0,
      };
    },
    mounted() {
      var self = this;

      this.$wamp.subscribe('badge.' + this.mac + '.lights_static', function(args, kwargs, details) {
        self.setLights(args);
      }, {}).then(function(s) {console.log("got it", s);});

      this.$wamp.subscribe('badge.' + this.mac + '.text', function(args, kwargs, details) {
        self.setText(args[0]);
      }, {}).then(function(s) {console.log("got it text", s);});
    },
    methods: {
      setLights: function(lights) {
          console.log(lights);
          for (var i in lights) {
            this.lights[3-i].r = (lights[i] >> 16) & 0xff;
            this.lights[3-i].g = (lights[i] >> 8) & 0xff;
            this.lights[3-i].b = lights[i] & 0xff;
          }
      },
      setText: function(text) {
          console.log("Text", text);

          this.text = text;
      },
      onButton: function(b) {
          console.log(this.show_screen);
          console.log(b);
          console.log(this.mac);
          this.$wamp.publish('badge_sim.button.press', [b], {update_id: this.update_id++, badge_id: this.mac});
      },
      onButtonUp: function(b) {
          console.log(b, "UP");
          this.$wamp.publish('badge_sim.button.release', [b], {update_id: this.update_id++, badge_id: this.mac});
      },
      onLights: function(args, kwargs) {
          console.log(args);
          console.log(kwargs);
      }
    }
  }
</script>
