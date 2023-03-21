<template>
    <div class="register">
      <NavBar navbartype='register' />
      <div class="registerbox">
        <form @submit.prevent="submitForm">
          <h3 class="registertitle">Register</h3>
          <p class="prompt">Username</p>
          <input type="text" class="userinput" v-model="username">
          <p class="error" v-if="errorDetected">{{ userError }}</p>
          <p class="prompt">Email</p>
          <input type="text" class="userinput" v-model="email">
          <p class="prompt">Password</p>
          <input type="password" class="userinput" v-model="password">
          <p class="error" v-if="errorDetected">{{ passError }}</p>
          <p class="prompt">Confirm Password</p>
          <input type="password" class="userinput" v-model="password2">
          <p class="error" v-if="errorDetected">{{ pass2Error }}</p>
          <button id="submit">Submit</button>
          <p class="switch">
          Already have an account?
          <router-link to="/login">Login here.</router-link> 
        </p>
        </form>
      </div>
    </div>
  </template>
  
  <style>
  .switch {
  margin-left: 15%;
  }
  .register {
    height: 100vh;
    background-color: #1A1D1A;
  }
  .registerbox {
    height: auto;
    width: 500px;
    margin: auto;
    margin-top: 4em;
    background-color: white;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
  }
  .registertitle {
    text-align: center;
    margin: 51px auto 30px;
    font-family: 'Inter', sans-serif;
    font-style: normal;
    font-weight: 700;
    font-size: 40px;
  }
  .prompt {
    margin-left: 15%;
    margin-bottom: 22px;
    font-family: 'Inter';
    font-style: normal;
    font-weight: 400;
    font-size: 20px;
  }
  .userinput {
    margin-left: 15%;
    margin-bottom: 22px;
    width: 330px;
    height: 45px;
    border-radius: 10px;
    font-size: large;
  }
  .error {
  margin-left: 15%;
  margin-bottom: 22px;
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  color: red;
}
  #submit {
    width: 330px;
    height: 55px;
    margin-left: 15%;
    margin-top: 10px;
    margin-bottom: 20px;
    border-radius: 30px;
  }
  </style>
  
  <script>
  import NavBar from '../components/NavBar.vue';

  import axios from 'axios'
  
  export default {
    name: "Register",
    components: {
      NavBar,
    },
    data () {
      return {
        username: "",
        email: "",
        password: "",
        password2: "",
        userError: "",
        passError: "",
        pass2Error: "",
        errorDetected: false,
      }
    },
    methods: {
        submitForm(){
          const formData = {
            username: this.username,
            email: this.email,
            password: this.password,
            password2: this.password2
          }
          axios
              .post('/api/account/register', formData)
              .then(response => {
                this.$router.push('/login')
                console.log(response)
              })
              .catch(error => {
                this.userError = ''
                this.passError = ''
                this.pass2Error = ''
                this.errorDetected = true
                if(error.response.data.username != undefined){
                  this.userError = error.response.data.username[0] 
                }
                if(error.response.data.password != undefined){
                  this.passError = error.response.data.password[0]
                }
                if(error.response.data.password2 != undefined){
                  this.pass2Error = error.response.data.password2[0]
                }
                if(error.response.data.non_field_errors != undefined){
                  this.pass2Error = error.response.data.non_field_errors[0]
                }
              })
              
        }
    }
  };
  </script>
  