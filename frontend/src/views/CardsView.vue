<template>
  <div class="container-gradient">
    <div class="container">
      <div class="row">
        <div class="col my-4  text-center">
          <div v-if="msg !== 'Active Cards'" class="alert alert-danger" role="alert">
            <h1>{{ msg }}</h1>
          </div>
          <div v-else-if="sortedCards.length <= 9" >
            <h1 class="text-white">Active Cards</h1>
            <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
              <div v-for="card in sortedCards" :key="card.id" class="col">
                <div class="card h-100">
                  <div class="card-body">
                    <h5 class="card-title">Id: {{ card.id }}</h5>
                    <p class="card-text">Card number: {{ card.card_number }}</p>
                    <div>
                      <button class="btn btn-secondary me-3" @click="openModifyCardModal(card)">Modify Card</button>
                      <button class="btn btn-danger" @click="deleteCard(card.id)">Delete Card</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
              <ul class="list-group">
                <li v-for="card in sortedCards" :key="card.id" class="list-group-item">
                  <div class="d-flex justify-content-between align-items-center p-2">
                  <div>
                    <div>ID: {{ card.id }}</div>
                    <div>Card number: {{ card.card_number }}</div>
                  </div>
                  <div><button class="btn btn-danger" @click="deleteCard(card.id)">Delete Card</button></div>
                </div>
                </li>
              </ul>
            </div>
          <button class="login-form-btn mt-4" @click="openAddCardModal">Add Card</button>
        </div>
      </div>

      <div v-if="showModifyCardModal" class="modal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Modify Card</h5>
              <button type="button" class="btn-close" @click="closeModifyCardModal"></button>
            </div>
            <form @submit.prevent="modifyCard">
              <div class="modal-body">
                <div class="mb-3">
                  <label for="cardNumber" class="form-label">Card Number</label>
                  <input type="text" class="form-control" id="cardNumber" v-model="cardNumber" required>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModifyCardModal">Close</button>
                <button type="submit" class="btn btn-primary">Modify Card</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div v-if="showAddCardModal" class="modal" tabindex="-1">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add Card</h5>
              <button type="button" class="btn-close" @click="closeAddCardModal"></button>
            </div>
            <form @submit.prevent="addCard">
              <div class="modal-body">
                <div class="mb-3">
                  <label for="cardNumber" class="form-label">Card Number</label>
                  <input type="text" class="form-control" id="cardNumber" v-model="cardNumber" required>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeAddCardModal">Close</button>
                <button type="submit" class="btn btn-success">Add Card</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
  import { ref, computed } from 'vue';
  import axios from 'axios';

  export default {
    setup() {
      const cards = ref([]);
      const cardNumber = ref('');
      const selectedCardId = ref(null);
      const showAddCardModal = ref(false);
      const showModifyCardModal = ref(false);
      const msg = ref('');
  
      const fetchCards = async () => {
        const response = await axios.get('http://127.0.0.1:5000/cards').
        catch((error) => {
          msg.value = error.response.data.message
        }).then((response) => {
          cards.value = response.data;
          msg.value = "Active Cards"
        });
      };

      const sortedCards = computed(() => {
        return cards.value.slice().sort((a, b) => a.id - b.id);
      });

      const openModifyCardModal = (card) => {
        selectedCardId.value = card.id;
        cardNumber.value = card.card_number;
        showModifyCardModal.value = true;
      };

      const closeModifyCardModal = () => {
        showModifyCardModal.value = false;
      };

      const openAddCardModal = () => {
        showAddCardModal.value = true;
      };
  
      const closeAddCardModal = () => {
        showAddCardModal.value = false;
      };

      const modifyCard = async () => {
        const data = {
          card_number: cardNumber.value,
        };

        const response = await axios.patch(`http://127.0.0.1:5000/cards/${selectedCardId.value}`, data)
        /*
        .catch((error) => {
          alert(error.response.data.message)
        }).then((response) => {
          alert(response.data.message)
        });*/

        await fetchCards();
        closeModifyCardModal();
      };
  
      const addCard = async () => {
        const data = {
          card_number: cardNumber.value,
        };

        const response = await axios.post('http://127.0.0.1:5000/cards', data)
        /*.catch((error) => {
          alert(error.response.data.message)
        }).then((response) => {
          alert(response.data.message)
        });*/
          
        await fetchCards();
        closeAddCardModal();
      };

      const deleteCard = async (id) => {
        const response = await axios.delete(`http://127.0.0.1:5000/cards/${id}`)
        /*.catch((error) => {
          alert(error.response.data.message)
        }).then((response) => {
          alert(response.data.message)
        });*/

        await fetchCards();
      };
  
      fetchCards();
  
      return {
        cards,
        msg,
        sortedCards,
        showAddCardModal,
        openModifyCardModal,
        closeModifyCardModal,
        openAddCardModal,
        closeAddCardModal,
        showModifyCardModal,
        addCard,
        modifyCard,
        deleteCard,
        cardNumber,
      };
    },
  };
</script>
  
<style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
</style>