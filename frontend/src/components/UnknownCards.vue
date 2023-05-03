<template>
  <div class="row">
    <div class="col my-4 mx-5">
      <div v-if="unknownCards.length < 1" class="alert alert-danger" role="alert">
        <h1>Cards not found</h1>
      </div>
      <div v-else-if="sortedCards.length <= 9">
        <div class="alert alert-success" role="alert">
          <h1>Inactive cards</h1>
        </div>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div v-for="unknownCard in unknownCards" :key="unknownCard.id" class="col">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title text-white">Id: {{ unknownCard.id }}</h5>
                <p class="card-text text-white">Card number: {{ unknownCard.card_number }}</p>
                <div class="d-flex flex-column align-items-center flex-md-row justify-content-md-center">
                  <button class="rounded-btn btn-success me-0 me-md-3 mb-2 mb-md-0" @click="activateCard(unknownCard.id)">Activate</button>
                  <button class="rounded-btn btn-danger" @click="deleteUnknownCard(unknownCard.id)">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-success" role="alert">
          <h1>Inactive cards</h1>
        </div>
        <div class="card-container">
        <ul class="list-group">
          <li v-for="unknownCard in sortedCards" :key="unknownCard.id" class="list-group-item">
            <div class="d-flex justify-content-between p-2">
              <div class="text-start">
                <div>ID: {{ unknownCard.id }}</div>
                <div>Card number: {{ unknownCard.card_number }}</div>
              </div>
              <div>
                <button class="btn btn-success me-3" @click="activateCard(unknownCard.id)">Activate</button>
                <button class="btn btn-danger" @click="deleteUnknownCard(unknownCard.id)">Delete Card</button>
              </div>
            </div>
          </li>
        </ul>
      </div>
      </div>
    </div>
  </div>
  <button class="login-form-btn my-4" @click="openAddCardModal">Add Card</button>

  <!-- Add Card Modal -->
  <div v-if="showAddCardModal" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Add Card</h5>
          <button type="button" class="btn-close" @click="closeAddCardModal"></button>
        </div>
        <form @submit.prevent="addUnknownCard">
          <div class="modal-body">
            <div class="mb-3">
              <label for="newCardNumber" class="form-label">Card Number</label>
              <input type="text" class="form-control" id="newCardNumber" v-model="newCardNumber" required>
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
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';

export default {
  emits: ['cardActivated'],
  setup(props, { emit }) {
    const unknownCards = ref([]);
    const newCardNumber = ref("");
    const showAddCardModal = ref(false);

    const fetchUnknownCards = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/unknown_cards');
        unknownCards.value = response.data;
      } catch (error) {
        if (error.response.status === 404) {
          unknownCards.value = [];
        } else {
          console.error(error);
        }
      }
    };

    const sortedCards = computed(() => {
      return unknownCards.value.slice().sort((a, b) => a.id - b.id);
    });

    const openAddCardModal = () => {
      showAddCardModal.value = true;
    };

    const closeAddCardModal = () => {
      showAddCardModal.value = false;
    };

    const addUnknownCard = async () => {
      uk_card_number: newCardNumber.value;

      const response = await axios.post(`http://127.0.0.1:5000/card_validation/${newCardNumber.value}`)
        .catch((error) => {
          if (error.response.status == 409) {
            alert(error.response.data.message)
          }
        });

      await fetchUnknownCards();
      closeAddCardModal();
    };

    const deleteUnknownCard = async (id) => {
      const response = await axios.delete(`http://127.0.0.1:5000/unknown_cards/${id}`).
        catch((error) => {
          if (error.response.status == 404) {
            alert(error.response.data.message)
          }
        });

      await fetchUnknownCards();
    };

    const activateCard = async (id) => {
      const response = await axios.post(`http://127.0.0.1:5000/activate_card/${id}`);
      emit('cardActivated');

      await fetchUnknownCards();
    };

    fetchUnknownCards();

    return {
      unknownCards,
      sortedCards,
      newCardNumber,
      showAddCardModal,
      openAddCardModal,
      closeAddCardModal,
      addUnknownCard,
      deleteUnknownCard,
      activateCard,
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
}
.alert{
  border-radius: 2rem;
  box-shadow: 0 5px 5px 5px rgba(0, 0, 0, 0.2);
}
.alert-success{
  background-color: rgba(128, 128, 128, 0.75);
  border-color: #808080;
  color: #fff;
}
.alert-danger{
  background-color: rgba(203, 11, 1, 0.75);
  border-color: #cb0b01;
  color: #fff;
}
.card {
  padding: 1rem 0;
  background-color: #413a63;
  font-weight: bold;
  border-radius: 2rem;
  box-shadow: 0 5px 5px 5px rgba(0, 0, 0, 0.2);
}
</style>