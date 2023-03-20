<template>
    <div class="site">
        <NavBar navbartype="login"/>
        <div class="content">
          <div class="mystuff">
            <div class="fpga" v-if="!showFullCatalog">
                <h2 class="fpgatitle">FPGA board connected</h2>
                <div class="sendbutton">Send games to board</div>
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
                <h2 class="switchtitle" :class="{active: showFullCatalog}" @click="showFullCatalog=false; getUserGames();">My Games</h2>
              </div>
              <div class="theList">
                <div v-for="game in allGames" :key="game.id" class="card">
                  <GameComp :info="game"/>
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
.content {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #ffffff;

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
  height: 90px;
  line-height: 90px;
  width: 288px;
  background-color: #6D8B9C;
  border-radius: 15px;
  font-size: 24px;
  margin-top: 20%;
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
        showFullCatalog: true
      }
    },
    methods: {
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
    }
};
</script>