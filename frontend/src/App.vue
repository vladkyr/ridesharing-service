<template>
  <div id="app">
    <div class="container-fluid">
      <div class="row">
        <div class="col-md-3">
            <Menu/>
        </div>
        <div class="col-md-9">
            <v-main transition="slide-x-transition">
                <router-view></router-view>
            </v-main>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Menu from './components/Menu.vue'

export default {
  name: 'App',
  components: {
    Menu
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  align-items: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
