<template>
    <div class="site">
      <NavBar navbartype="faq"/>
        <div class="content">
          <div class="mystuff">
            <div class="fpga" v-if="!showFullCatalog">
                <h2 class="fpgatitle">FPGA board connected</h2>
                <div @click="syncWithFPGA" class="sendbutton">Sync with board</div>
                <p v-if="sentConfirmation">Successfully synced!</p>
                <div class="fpgainfo">
                  <h2>Current Storage: {{ currfileSize }}</h2>
                  <h2>Total Storage: {{ totfileSize }}</h2>
                  
                </div>
                <div class="filter">
                  <label class="labeltitle" for="menu">Select a filter:</label>
                  <div class="filterops">
                    <select id="menu" name="menu">
                      <option value="option4">None</option>
                      <option value="option1">Category</option>
                      <option value="option2">Manufacturer</option>
                      <option value="option3">Game Type</option>
                    </select>
                  </div>
                </div>
            </div>
            <div class="mygames" v-if="!showFullCatalog">
              <div class="switchTitles">
                <h2 class="switchtitle" :class="{active: showFullCatalog}" @click="showFullCatalog=true; getAllGames();">Catalog</h2>
                <h2 class="switchtitle" @click="showFullCatalog=false">My Games</h2>
              </div>
                <div class="myList">
                  <div v-for="game in allGames" :key="game.id" class="card">
                    <GameComp :info="game"/>
                  </div>
                </div>
              <div class="nextPrev">
                <p @click="prevAllGames" class="movepage">Prev</p>
                <p @click="nextAllGames" class="movepage">Next</p>
              </div>
            </div>
            <div class="catalog" v-if="showFullCatalog">
              <div class="switchTitles">
                <h2 class="switchtitle" :class="{active: showFullCatalog}" @click="showFullCatalog=true">Catalog</h2>
                <h2 class="switchtitle" :class="{active: showFullCatalog}" @click="showFullCatalog=false; getUserGames(); sentConfirmation=false;">My Games</h2>
              </div>
              <div class="theList">
                <div v-for="game in allGames" :key="game.id" class="card">
                  <GameComp :info="game" :added="false" :fullCatalog="showFullCatalog"/>
                </div>
              </div>
              <div class="nextPrev">
                <p @click="prevAllGames" class="movepage">Prev</p>
                <p @click="nextAllGames" class="movepage">Next</p>
              </div>
            </div>
          </div>
        </div>
    </div>
</template>

<style>
.site {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #1A1D1A;
}
.filter{
  display: flex;
  flex-direction: row;
  /* background-color: #6D8B9C; */
  color: white;
  height: 30px;
  width: 288px;
  justify-content: bottom;
  margin-top:5%;
  margin-bottom: 10%;
  border-radius: 10px;
}
.labeltitle{
  display: flex;
  justify-content: top;
  margin-top: 0px;
  font-size: medium;
  font-style: bold;
  width: 100px;
  color: black;
  padding-right: 20px;
  padding-bottom: 20px;
}
.filterops {
  font-size: 16px;
  border: none;
  cursor: pointer;
  height: 30px;
  padding-right:20px;
  justify-content: bottom;
}

/* Dropdown button on hover & focus */
/* .dropbtn:hover, .dropbtn:focus {
} */

/* The container <div> - needed to position the dropdown content */
.dropdown {
  position: relative;
  display: inline-block;
}

/* Dropdown Content (Hidden by Default) */
.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}
.fpgainfo{
  padding:20px;
  padding-top:10px;
}
.content {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #ffffff;
    padding-bottom: 30px;

}
.myGamestitle{
  padding-left:20px;
}
.mystuff {
    display: flex;
    flex-direction: row;
    height: 400px;
    /*background-color: red;*/
    margin: 20px;
}
.fpga {
    display: flex;
    flex-direction: column;
    width: 20%;
}
.fpgatitle {
    width: 40%;
    padding:20px;
}
.switchtitle {
  margin-left: 20px;
  cursor: pointer;
  color: #506472;
}

.switchtitle:hover{
  color: lightblue;
}

.switchtitle:active {
  color: blue;
}

.switchTitles{
  display: flex;
  flex-direction: row;
}
.sendbutton {
    text-align: center;
    vertical-align: middle;
    height: 30px;
    line-height: 60px;
    width: 200px;
    background-color: #6D8B9C;
    border-radius: 15px;
    font-size: 24px;
    margin-top: 10%;
    padding-bottom: 10%;
    cursor: pointer;
}
.myList{
  display: grid;
  grid-template-columns: 5fr 5fr 5fr 5fr 5fr 5fr;
  grid-template-rows: 5fr 5fr;
  column-gap: 1rem;
  margin: 0 auto;
}
.theList{
  display: grid;
  grid-template-columns: 5fr 5fr 5fr 5fr 5fr 5fr;
  grid-template-rows: 5fr 5fr;
  column-gap: 1rem;
  margin: 0 auto;
}
.card {
  width: 186px;
  border-radius: .5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.catalog {
  width: 80%;
  margin: auto;
}
.nextPrev{
  display: flex;
  flex-direction: row;
  margin: 10px
}
.movepage{
  cursor: pointer;
  margin: 20px;
}
</style>

<script>
  import myGames from "../assets/userGames.json"
  import allGames from "../assets/catalogGames.json"
  import GameComp from "../components/GameComp.vue";
  import NavBar from "../components/NavBar.vue";
  import axios from 'axios'
  var myFunction = function() {
      document.getElementById("myDropdown").classList.toggle("show");
  }

  export default {
    name: "HomePage",
    components: {
      NavBar,
      GameComp
    },
    data () {
      return {
        allGames: allGames,
        nextPageURL: null,
        prevPageURL: null,
        showFullCatalog: true,

        total_storage: null,
        current_storage:null,
        sentConfirmation: false,
      }
    },
    computed: {
      currfileSize() {
      // Check if file size is less than 1000 MB
      if (this.convertFileSize(this.current_storage) < 1000) {
        return `${this.convertFileSize(this.current_storage)} MB`;
      }
      // Call the convertFileSize function and return the size in GB with the appropriate unit
      const sizeInGB = this.convertFileSize2(this.current_storage);
      return `${sizeInGB} GB`;
    },
    totfileSize() {
      // Check if file size is less than 1000 MB
      if (this.convertFileSize(this.total_storage) < 1000) {
        return `${this.convertFileSize(this.total_storage)} MB`;
      }
      // Call the convertFileSize function and return the size in GB with the appropriate unit
      const sizeInGB = this.convertFileSize2(this.total_storage);
      return `${sizeInGB} GB`;
    }
    },
    methods: {
      convertFileSize(sizeInB) {
      // Convert size to GB
      const sizeInGB = sizeInB / 1024;
      // Round off to two decimal places
      const roundedSizeInGB = Math.round(sizeInGB * 100) / 100;
      return roundedSizeInGB;
    },
    convertFileSize2(sizeInMB) {
      // Convert size to GB
      const sizeInGB = sizeInMB / (1024*1024);
      // Round off to two decimal places
      const roundedSizeInGB = Math.round(sizeInGB * 100) / 100;
      return roundedSizeInGB;
    },

      syncWithFPGA(){
        this.sentConfirmation = false;
        axios.put('/api/account/UserSync', {data:{sync_flag: true}}).then((response) =>{
          this.sentConfirmation = true
        })
      },
      getUserGames(){
        this.$http.get('/api/account/user_game').then((response) =>{
          console.log(response)
          this.allGames = response.data.results
          this.nextPageURL = response.data.next.slice(16)
        })
        .catch((err) =>{
          console.log(err)
        })
      },
      getUserStorage(){
        this.$http.get('/api/account/current_storage').then((response) =>{
          console.log(response)
          this.total_storage = response.data.total_storage
          this.current_storage = response.data.current_storage
        })
        .catch((err) =>{
          console.log(err)
        })
      },
      getAllGames(){
        this.$http.get('/api/games/all-games').then((response) =>{
          console.log(response)
          this.allGames = response.data.results
          this.nextPageURL = response.data.next.slice(16)
        })
        .catch((err) =>{
          console.log(err)
        })
      },
      nextAllGames(){
        if(this.nextPageURL != null){
        this.$http.get(this.nextPageURL).then((response) =>{
          console.log(response)
          this.allGames = response.data.results
          if(response.data.next != null){
            this.nextPageURL = response.data.next.slice(16)
          }
          this.prevPageURL = response.data.previous.slice(16)
          console.log(this.prevPageURL)
        })
        .catch((err) =>{
          console.log(err)
        })
      }
      }, 
      prevAllGames(){
        if(this.prevPageURL != null){
          this.$http.get(this.prevPageURL).then((response) =>{
          console.log(response)
          this.allGames = response.data.results
          this.nextPageURL = response.data.next.slice(16)
          if(response.data.previous != null){
            this.prevPageURL = response.data.previous.slice(16)
          }
        })
        .catch((err) =>{
          console.log(err)
        })
        }
      }
    },
    created(){
      this.getAllGames()
      this.getUserGames()
      this.getUserStorage()
    },
    addjob: function() {
    myFunction();
    
    }
   
};
</script>
