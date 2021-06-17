<template>
    <div class="init-db-menu">
        <div class="menu-row">
            <button class="button" @click="initDatabase">initialise DB</button>
        </div>
        <div class="menu-row">
            <button class="button" @click="fillDatabase">fill DB</button>
        </div>
        <p>{{payload.message}}</p>
        <p v-if="error_bool">{{helper}}</p>
        <p v-if="error_bool">{{error_msg}}</p>
    </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'InitDB',
  props: {
    msg: String
  },
  methods: {
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
<style scoped></style>

