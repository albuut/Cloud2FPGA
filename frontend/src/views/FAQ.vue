<template>
  <div class="site">
    <NavBar navbartype="catalog"/>
      <div class="content">
        <div class="overview" >
          <h1 class="overviewtitle" id="box">Overview</h1>
          <h3 class="overviewinfo">MiSTer is an open source project that aims to recreate various classic arcade machines, computers,
            and game consoles using modern hardware. It allows software and game images to run as they would on original hardware,
            using peripherals such as mice, keyboards, joysticks, and other game controllers. MiSTer utilizes an FPGA board called 
            'DE10-Nano' which connects to your TV or monitor via HDMI video out. <br><br>
            
            This website serves as a way to easily choose which games you would like to play. Simply click the "Add" button on a game
            you want to play and it will be added to your "My Games" page. You can add up to ____ games. When you are ready to upload
            your games to your FPGA device click the button "Sync with board" and the games will automatically upload. You can unadd
            the games from your "My Games" page as well. To switch from the "Catalog" page to "My Games" page simply click the word
            at the top. <br><br>

            To log out click on the Cloud2FPGA icon at the top left!
            </h3>
        </div>
        <div class="setup">
            <h1 class="setuptitle" id="box">How To Set MiSTer Up</h1>
            <h3 class="setupinfo">Follow this link for a set up guide! <br>
            <a href="https://www.youtube.com/watch?v=sMsonyMgzoY&t=72s"> MiSTer Setup</a></h3>
        </div> 
        <div class="script">
            <h1 class="scripttitle" id="box">Where To Put Download Script</h1>
            <h3 class="scriptinfo">Drag and drop the cloud2fpga folder into the Scripts directory. You will be able to toggle the script
              on and off in the scripts menu. The script needs to be turned on every time the MiSTer reboots. </h3>
            </div>   
        <div class="errors">
            <h1 class="errorstitle" id="box">Common Errors</h1>
            <h3 class="errorsinfo">here is all the info for common errors</h3>
        </div>
        <div class="wiki">
         <h3 >For more information visit <a href="https://github.com/MiSTer-devel/Wiki_MiSTer/wiki">Official MiSTer Wiki</a> </h3>  
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

.wiki{
  position: absolute;
  bottom: 20px;
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
  padding-bottom: 50px;
}
.scriptinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 50px;
}
.setupinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 50px;
}
.errorsinfo{
  display: flex;
  padding-top: 10px;
  padding-bottom: 50px;
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