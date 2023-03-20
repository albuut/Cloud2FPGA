<template>
    <div class="navbar">
        <router-link to="/" class="homelink">
            <img src="../assets/logo.png" class="logo">
            <h1 class="title">Cloud2FPGA</h1>
        </router-link>
        <div class="menu">
            <router-link to="/login"><div v-if="navbartype ==='home'" class="button">Get Started</div></router-link>
            <router-link to="/faq"><div v-if="navbartype ==='faq'" class="button">FAQ</div></router-link>
            <router-link to="/catalog"><div v-if="navbartype ==='catalog'" class="button">Catalog</div></router-link>
        </div>
      
    </div>
</template>

<script>
export default {
    props: {
        navbartype: String
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inria+Sans&display=swap');
.navbar {
    display: flex;
    flex: 0 1 64px;
    justify-content: flex-start;
}
.homelink {
    display: flex;
    flex-direction: row;
}
.logo {
    width: 64px;
    height: auto;
}
.title {
    font-size: 24pt;
    font-family: 'Inria Sans', sans-serif;
    margin-top: auto;
    margin-bottom: auto;
    color: #8AB0AB;
}
.menu {
    margin: auto 2rem auto auto;
}
.button {
    width: 130.67px;
    height: 44px;
    border: 3px solid #8AB0AB;
    border-radius: 10px;
    font-family: 'Inria Sans', sans-serif;
    text-align: center;
    font-size: 16pt; 
    color: #8AB0AB;
    line-height: 44px;
    justify-self: right;
    
}

a {
    text-decoration: none;
}
</style>