<template>
  <div class="menu">
    <b-nav vertical>
        <b-nav-item active to="/">Home</b-nav-item>
        <h5 class="menu-section">Mysql:</h5>
        <b-nav-item active to="/init-db">Init DB</b-nav-item>
        <b-nav-item active to="/book-ride?database=mysql">Book ride</b-nav-item>
        <b-nav-item active to="/report?database=mysql">Report</b-nav-item>
        <b-nav-item active to="/migrate">Migrate</b-nav-item>
        <h5 class="menu-section">Nosql:</h5>
        <b-nav-item active to="/book-ride?database=mongo">Book ride</b-nav-item>
        <b-nav-item active to="/report?database=mongo">Report</b-nav-item>
    </b-nav>
    <p>{{payload.message}}</p>
    <p v-if="error_bool">{{helper}}</p>
    <p v-if="error_bool">{{error_msg}}</p>
    <p class="copyright">&copy; Vladyslav Kyryk</p>
  </div>
</template>

<script>
export default {
  name: 'Menu',
  props: {
    msg: String
  },
  methods: {},
  data(){
    return{
        payload: [],
        helper: "",
        error_msg: "",
        error_bool: null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
b-nav-item {
    font-size: 18px;
}
.copyright {
    margin-top: 200px;
}
</style>
