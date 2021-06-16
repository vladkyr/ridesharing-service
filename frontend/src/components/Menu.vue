<template>
  <div class="menu">
    <div class="container-fluid">
        <div class="menu-row">
            <button class="button" @click="initDatabase">initialise DB</button>
        </div>
        <div class="menu-row">
            <button class="button" @click="fillDatabase">fill DB</button>
        </div>
        <div class="menu-row">
            <button class="button" @click="getReport">get report</button>
        </div>
        <div class="menu-row">
            <button class="button" @click="bookRide">book ride</button>
        </div>
    </div>
    <p>{{payload.message}}</p>
    <p v-if="error_bool">{{helper}}</p>
    <p v-if="error_bool">{{error_msg}}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Menu',
  props: {
    msg: String
  },
  methods: {
      handleButtonClick() {
        console.log("clicked button")
        this.error_bool = false
        axios.get('http://localhost:8000/home')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    },
    initDatabase() {
        console.log("clicked init DB button")
        this.error_bool = false
        axios.get('http://localhost:8000/init-db')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "init DB button -> something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    },
    fillDatabase() {
        console.log("clicked fill DB button")
        this.error_bool = false
        axios.get('http://localhost:8000/fill-db')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "fill DB button -> something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    },
    getReport() {
        console.log("clicked report button")
        this.error_bool = false
        axios.get('http://localhost:8000/report')
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "get report button -> something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    },
    bookRide() {
        console.log("clicked book ride button")
        this.error_bool = false
        axios.get('http://localhost:8000/book-ride')
        axios({
          method: 'post',
          url: 'http://localhost:8000/book-ride',
          data: {
            firstName: 'Fred',
            lastName: 'Flintstone'
          }
        })
        .then((response) => {
            this.payload = response.data
            console.log(response.data)
            this.clicked = "clicked"
      })
      .catch(error => {
          this.payload = {'message': "book ride button -> something went wrong! Your Api isn't running properly."}
          this.error_bool = true
          this.helper = "right click -> Inspect -> Console. Check the console error message after button click"
          this.error_msg = error
      })
    }
  },
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
