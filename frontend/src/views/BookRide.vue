<template>
    <div class="book-ride-menu">
        <b-container fluid>
            <label class="input-header">Please fill in the fields to book a ride:</label>
            <b-row class="input">
                <b-col sm="3">
                    <label>email:</label>
                </b-col>
                <b-col sm="4">
                    <b-form-input v-model="email" :type="email"></b-form-input>
                </b-col>
            </b-row>
            <b-row class="input">
                <b-col sm="3">
                    <label>password:</label>
                </b-col>
                <b-col sm="4">
                    <b-form-input v-model="password" :type="password"></b-form-input>
                </b-col>
            </b-row>
            <b-row class="input">
                <b-col sm="3">
                    <label>start location:</label>
                </b-col>
                <b-col sm="4">
                    <b-form-input v-model="start"></b-form-input>
                </b-col>
            </b-row>
            <b-row class="input">
                <b-col sm="3">
                    <label>destination:</label>
                </b-col>
                <b-col sm="4">
                    <b-form-input v-model="dest"></b-form-input>
                </b-col>
            </b-row>
            <b-row class="input">
                <b-col sm="3">
                    <label>passengers:</label>
                </b-col>
                <b-col sm="4">
                    <b-form-input v-model="passengers" :type="number"></b-form-input>
                </b-col>
            </b-row>
        </b-container>
        <div class="menu-row">
            <button class="button" id="book-ride-button" @click="bookRide">book ride</button>
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
        axios.post('http://localhost:8000/book-ride', {
            email: this.email,
            password: this.password,
            start: this.start,
            dest: this.dest,
            passengers: this.passengers
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