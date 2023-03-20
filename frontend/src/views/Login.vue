<template>
  <div class="login">
    <NavBar navbartype='login' />
    <div class="loginbox">
      <form @submit.prevent="submitForm">
        <h3 class="logintitle">Login</h3>
        <p class="prompt">Username</p>
        <input type="text" class="userinput" v-model="username">
        <p class="prompt">Password</p>
        <input type="password" class="userinput" v-model="password">
        <button type="submit" id="submit">Log in</button>
        <p class="switch">
          Don't have an account?
        <router-link to="/register">Register here.</router-link> 
        </p>
      </form>
    </div>
  </div>
</template>

<style>
.switch {
  margin-left: 15%;
  margin-bottom: 22px;
}
.login {
  height: 100vh;
  background-color: #1A1D1A;
}
.loginbox {
  height: 670px;
  width: 500px;
  margin: auto;
  margin-top: 4em;
  background-color: white;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}
.logintitle {
  text-align: center;
  margin: 51px auto 55px;
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
#submit {
  width: 330px;
  height: 55px;
  margin-left: 15%;
  margin-top: 30px;
  border-radius: 30px;
}
</style>

<script>
import NavBar from '../components/NavBar.vue';
import axios from 'axios'

export default {
  name: "Login",
  components: {
    NavBar,
},
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submitForm(){
      const formData = {
        username: this.username,
        password: this.password 
      }

      axios
        .post('/api/account/login', formData)
        .then(response => {
          console.log(response)

          const token = response.data.token

          this.$store.commit('setToken', token)

          axios.defaults.headers.common['Authorization'] = 'Token ' + token

          localStorage.setItem('token', token)
          //testing
          //console.log(localStorage.getItem('token'))
          //console.log(this.$store.state.token)
          this.$router.push('/catalog')
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created: function () {
    
  }
};
</script>
