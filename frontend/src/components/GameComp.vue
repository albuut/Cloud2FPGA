<template>
    <div class="modal-backdrop">
      <div class="modal">
        <header class="modal-header">
          <div name="header">{{ info.game_name}}
          </div>
          <div class="platandYear">
            <p class="plat">{{info.game_year}}</p>
          </div>
        </header>
  
        <div class="modal-body">
          <img class="boxart" :src="info.cover" alt="boxart not found">
         </div>
  
        <footer class="modal-footer" v-if="fullCatalog">
          <button
            type="button"
            class="add-btn"
            @click="addToUserGames"
            v-if="!added"
          >
          Add
          </button>
          <div v-else class="add-btn1">Added</div>
        </footer>
        <footer class="modal-footer" v-else>
          <button
            type="button"
            class="add-btn"
            @click="unaddToUserGames"
            v-if="!added"
          >
          Unadd
          </button>
          <div v-else class="add-btn1">Unadded</div>
        </footer>
      </div>
    </div>
</template>
<script>
import axios from 'axios';
export default {

  props: {
      info: Object,
      added: Boolean,
      fullCatalog: Boolean,
  },
  data () {
      return {
      }
    },
  methods: {
    addToUserGames(){
      const formData = {
        game_name : this.info.game_name
      }
      axios.post('/api/parent/1/child/create/', formData).then((response) =>{
        this.added = true
      })
    },
    unaddToUserGames(){
      var game_name_ = this.info.game_name
      axios.delete('/api/parent/1/child/create/', {data:{game_name : game_name_}}).then((response) =>{
        this.added = true
      })
    }
  }
}
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inria+Sans&display=swap');
  .modal-backdrop {
    width:187px;
    background-color: #1a1d1a;
    justify-content: center;
    align-items: center;
    border-radius: 15px;
  }

  .modal {
    display: flex;
    flex-direction: column;
  }
  .modal-header {
    font-family: 'Inria Sans', sans-serif;
    position: relative;
    font-size: 16px;
    text-align: center;
    margin-top: 10px;
  }
  .platandYear {
    display: flex;
    width: 100%;
    flex-direction: row;
    margin-top: 10px;
  }
  .plat {
    margin-right: 25px;
    margin: auto;
    text-align: center;
  }

  .modal-footer {
    font-size: 16px;
    text-align: center;
    display: flex;
  }

  .modal-header {
    position:relative;
    text-align: center;
    color: white;
  }

  .modal-body {
    position: relative;
    height: 160px;
  }

  .add-btn {
    font-family: 'Inria Sans', sans-serif;
    color: #FFFFFF;
    border: #1A1D1A;
    background-color: #26413C;
    cursor: pointer;
    font-size: 20px;
    font-style: bold;
    height:34.68px;
    width:84.9px;
    margin: auto;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .add-btn1 {
    font-family: 'Inria Sans', sans-serif;
    color: #FFFFFF;
    border: #1A1D1A;
    cursor: pointer;
    font-size: 20px;
    font-style: bold;
    height:34.68px;
    width:84.9px;
    margin: auto;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .boxart{
    display: block;
    max-width: 100%;
    max-height: 160px;
    margin: auto;
  }
</style>