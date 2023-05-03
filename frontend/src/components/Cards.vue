<template>
  <div class="row">
    <div class="col mt-4 mb-2 mx-5">
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
                <i v-if="isCardReserved(card.id)" class="fa fa-minus-circle float-end" type="button" @click="disconnectCardFromUser(card.id)"></i>
                <i v-else class="fa fa-plus-circle float-end" type="button" @click="openConnectModal(card.id)"></i>
                <h5 class="card-title">Id: {{ card.id }}</h5>
                <p class="card-text">Card number: {{ card.card_number }}</p>
                <div>
                  <button class="btn btn-secondary me-3" @click="openModifyCardModal(card)">Modify</button>
                  <button class="btn btn-danger" @click="deleteCard(card.id)">Delete</button>
                  <div v-if="isCardReserved(card.id)">
                    <hr>
                    <p>{{ whoIsCardConnectedTo(card.id)}}</p>
                  </div>
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
        <div class="card-container">
        <ul class="list-group">
          <li v-for="card in sortedCards" :key="card.id" class="list-group-item">
            <div class="d-flex justify-content-between p-2">
              <div class="text-start">
                <div>ID: {{ card.id }}</div>
                <div>Card number: {{ card.card_number }}</div>
              </div>
              <div>
                <button class="btn btn-secondary me-3" @click="openModifyCardModal(card)">Modify</button>
                <button class="btn btn-danger" @click="deleteCard(card.id)">Delete Card</button>
                <i class="fa fa-plus-circle"></i>
                
              </div>
            </div>
          </li>
        </ul>
        </div>
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

  <!-- Connect Modal -->
  <div v-if="showConnectModal" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Connect Card to User</h5>
          <button type="button" class="btn-close" @click="closeConnectModal"></button>
        </div>
        <form @submit.prevent="connectCardToUser(selectedUserId)">
          <div class="modal-body">
            <div class="mb-3">
              <label for="userSelect" class="form-label">Select User</label>
              <select class="form-select" id="userSelect" v-model="selectedUserId" required>
                <option disabled value="">Please select a user</option>
                <option v-for="user in unassignedUsers" :key="user.id" :value="user.id">
                  {{ user.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeConnectModal">Close</button>
            <button type="submit" class="btn btn-primary">Connect Card</button>
          </div>
        </form>
      </div>
    </div>
  </div>

</template>
<script>
import { ref, computed, watchEffect } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const users = ref([]);
    const cards = ref([]);
    const userCards = ref([]);
    const unassignedUsers = ref([]);
    const cardNumber = ref('');
    const selectedCardId = ref(null);
    const showModifyCardModal = ref(false);
    const showInfo = ref(false);
    const msg = ref('');
    const selectedUserId = ref('');

    // User card connection
    const showConnectModal = ref(false);
    const showDisconnectModal = ref(false);
    const selectedCardIdForConnect = ref(null);
    const selectedCardIdForDisconnect = ref(null);

    const fetchCards = async () => {
        const response = await axios.get('http://127.0.0.1:5000/cards')
        .then((response) => {
          msg.value = "Active Cards"
          cards.value = response.data;
        })
        .catch((error) => {
          if (error.response.status === 404) {
            msg.value = "Cards not found"
            cards.value = []
          } else {
            console.error(error)
          }
        });
    };

    const fetchUsers = async () => {
      const response = await axios.get("http://127.0.0.1:5000/users");
      users.value = response.data;
    };

    const fetchUserCards = async () => {
      const response = await axios.get('http://127.0.0.1:5000/user_cards').
      then((response) => {
        userCards.value = response.data;
      }).
      catch((error) => {
        if (error.response.status === 404) {
          console.log("User cards not found")
        } else {
          console.error(error)
        }
      })
    };


    const isCardReserved = (cardId) => {
      return userCards.value.some((userCard) => userCard.card_id === cardId);
    };

    const sortedCards = computed(() => {
      return cards.value.slice().sort((a, b) => a.id - b.id);
    });

    const whoIsCardConnectedTo = (cardid) => {
      const usercard_user_id = userCards.value.find((userCard) => userCard.card_id === cardid).user_id;
      const user = users.value.find((user) => user.id === usercard_user_id);
      return user.name;
    };
    
    const openModifyCardModal = (card) => {
      selectedCardId.value = card.id;
      cardNumber.value = card.card_number;
      showModifyCardModal.value = true;
    };

    const closeModifyCardModal = () => {
      showModifyCardModal.value = false;
    };

    const openConnectModal = (cardId) => {
      selectedCardIdForConnect.value = cardId;
      showConnectModal.value = true;
    };

    const closeConnectModal = () => {
      showConnectModal.value = false;
    };

    const modifyCard = async () => {
      const data = {
        card_number: cardNumber.value,
      };
      const response = await axios.patch(`http://127.0.0.1:5000/cards/${selectedCardId.value}`, data);
      await fetchCards();
      closeModifyCardModal();
    };

    const deleteCard = async (id) => {
      const userCard = userCards.value.find((uc) => uc.card_id === id);
      if (userCard) {
        alert("This card is currently connected to a user. Please disconnect it before deleting.");
        return;
      }
      const response = await axios.delete(`http://127.0.0.1:5000/cards/${id}`);
      await fetchCards();
    };
    

    const connectCardToUser = async (userId) => {
    const response = await axios.post(`http://127.0.0.1:5000/user_cards`, {
        card_id: selectedCardIdForConnect.value,
        user_id: userId,
      });
      await fetchUserCards();
      closeConnectModal();
    };

    const disconnectCardFromUser = async (cardid) => {
      const del_userCard = userCards.value.find((uc) => uc.card_id === cardid);
      const response = await axios.delete(
        `http://127.0.0.1:5000/user_cards/${del_userCard.id}`
      );
      location.reload();
      await fetchUserCards();
    };

    const checkUserAssignment = () => {
  unassignedUsers.value = [];
  if (userCards.value.length === 0) {
    users.value.forEach((user) => {
      unassignedUsers.value.push(user);
    });
  } else {
    users.value.forEach((user) => {
      const userCard = userCards.value.find((uc) => uc.user_id === user.id);
      if (!userCard) {
        unassignedUsers.value.push(user);
      }
    });
  }
};

watchEffect(() => {
  if (userCards.value.length > 0 && users.value.length > 0) {
    checkUserAssignment();
  } else if (users.value.length > 0) {
    users.value.forEach((user) => {
      unassignedUsers.value.push(user);
    });
  }
});

    fetchUsers();
    fetchCards();
    fetchUserCards();
    isCardReserved();

    return {
      cards,
      users,
      userCards,
      msg,
      sortedCards,
      openModifyCardModal,
      closeModifyCardModal,
      showModifyCardModal,
      openConnectModal,
      closeConnectModal,
      showConnectModal,
      showDisconnectModal,
      connectCardToUser,
      disconnectCardFromUser,
      selectedUserId,
      modifyCard,
      deleteCard,
      cardNumber,
      fetchCards,
      fetchUserCards,
      isCardReserved,
      unassignedUsers,
      whoIsCardConnectedTo,
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