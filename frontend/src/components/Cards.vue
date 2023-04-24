<template>
  <div class="row">
    <div class="col my-4">
      <div v-if="msg !== 'Active Cards'" class="alert alert-danger" role="alert">
        <h1>{{ msg }}</h1>
      </div>
      <div v-else-if="sortedCards.length <= 9">
        <div class="alert alert-success" role="alert">
          <h1>{{ msg }}</h1>
        </div>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div v-for="card in sortedCards" :key="card.id" class="col">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">Id: {{ card.id }}</h5>
                <p class="card-text">Card number: {{ card.card_number }}</p>
                <div>
                  <button class="btn btn-secondary me-3" @click="openModifyCardModal(card)">Modify</button>
                  <button class="btn btn-danger" @click="deleteCard(card.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-success" role="alert">
          <h1>{{ msg }}</h1>
        </div>
        <ul class="list-group">
          <li v-for="card in sortedCards" :key="card.id" class="list-group-item">
            <div class="d-flex justify-content-between p-2">
              <div class="text-start">
                <div>ID: {{ card.id }}</div>
                <div>Card number: {{ card.card_number }}</div>
              </div>
              <div>
                <button class="btn btn-danger" @click="deleteCard(card.id)">Delete Card</button>
              </div>
            </div>
          </li>
        </ul>
      </div>
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
</template>
<script>
import { ref, computed } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const cards = ref([]);
    const cardNumber = ref('');
    const selectedCardId = ref(null);
    const showModifyCardModal = ref(false);
    const msg = ref('');

    const fetchCards = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/cards')
        msg.value = "Active Cards"
        cards.value = response.data;
      } catch (error) {
        if (error.response.status === 404) {
          msg.value = "Cards not found"
          cards.value = []
        } else {
          console.error(error)
        }
      }
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

    const modifyCard = async () => {
      const data = {
        card_number: cardNumber.value,
      };
      const response = await axios.patch(`http://127.0.0.1:5000/cards/${selectedCardId.value}`, data)
      await fetchCards();
      closeModifyCardModal();
    };

    const deleteCard = async (id) => {
      const response = await axios.delete(`http://127.0.0.1:5000/cards/${id}`)
      await fetchCards();
    };

    fetchCards();

    return {
      cards,
      msg,
      sortedCards,
      openModifyCardModal,
      closeModifyCardModal,
      showModifyCardModal,
      modifyCard,
      deleteCard,
      cardNumber,
      fetchCards,
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