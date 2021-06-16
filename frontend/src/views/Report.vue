<template>
    <div class="rows">
        <div class="menu-row">
            <button class="button" @click="getReport">get report</button>
        </div>
        <p>{{payload.message}}</p>
        <p v-if="error_bool">{{helper}}</p>
        <p v-if="error_bool">{{error_msg}}</p>
    </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'GetReport',
  props: {
    msg: String
  },
  methods: {
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

