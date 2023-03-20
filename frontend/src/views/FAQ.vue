<template>
  <div class="site">
    <NavBar navbartype="catalog"/>
      <div class="content">
        <div class="overview" >
          <h1 class="overviewtitle" id="box">Overview</h1>
          <h3 class="overviewinfo">here is all the info for overview</h3>
        </div>
        <div class="setup">
            <h1 class="setuptitle" id="box">How To Set MiSTeR Up</h1>
            <h3 class="setupinfo">here is all the info for setup</h3>
        </div> 
        <div class="script">
            <h1 class="scripttitle" id="box">Where To Put Download Script</h1>
            <h3 class="scriptinfo">here is all the info for script</h3>
        </div>   
        <div class="errors">
            <h1 class="errorstitle" id="box">Common Errors</h1>
            <h3 class="errorsinfo">here is all the info for common errors</h3>
        </div>  
      </div>
  </div>
</template>

<style>
#box{
  height: 50px;
  width: 900px;
  position: relative;
  border-bottom: 3px solid;
}
.site {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #1A1D1A;
}


.content {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #ffffff;
    padding-left: 30px;

}
.overviewinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 100px;
}
.scriptinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 100px;
}
.setupinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 100px;
}
.errorsinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 100px;
}
.overviewtitle{
  padding-top: 20px;  
}
.scripttitle{
  padding-top: 20px;
  border-bottom: solid;
}
.setuptitle{
  padding-top: 20px;
  border-bottom: solid;
}
.errorstitle{
  padding-top: 20px;
  border-bottom: solid;
}
</style>

<script>
 import NavBar from "../components/NavBar.vue";
 export default {
  name: "HomePage",
        components: {
          NavBar
        }
 }
</script>