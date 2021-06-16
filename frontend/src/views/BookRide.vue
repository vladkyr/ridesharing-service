<template>
    <div class="rows">
        <div class="menu-row">
            <button class="button" @click="bookRide">book ride</button>
        </div>
        <p>{{payload.message}}</p>
        <p v-if="error_bool">{{helper}}</p>
        <p v-if="error_bool">{{error_msg}}</p>
    </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'BookRide',
  props: {
    msg: String
  },
  methods: {
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
<style scoped></style>