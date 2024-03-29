<template>
    <div class="row">
        <div class="col my-4 mb-2 mx-5">
            <div v-if="msg !== 'ACTIVE CARDS'" class="alert alert-danger rounded rounded-3" role="alert">
                <h1>{{ msg }}</h1>
            </div>
            <div v-else-if="sortedCards.length <= 9">
                <div class="alert alert-success rounded rounded-3" role="alert">
                    <h1>{{ msg }}</h1>
                </div>
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    <div v-for="card in sortedCards" :key="card.id" class="col">
                        <div class="card rounded rounded-3">
                            <div class="card-body">
                                <div>
                                    <i v-if="isCardReserved(card.id)" class="fa fa-minus-circle float-end"
                                    type="button" @click="disconnectCardFromUser(card.id)"></i>
                                    <i v-else class="fa fa-plus-circle float-end" type="button" @click="openConnectModal(card.id)"></i>
                                </div>

                                <div class="text-center mb-3">
                                    <h5 class="card-title">Id: {{ card.id }}</h5>
                                    <p class="card-text">Card number: {{ card.card_number }}</p>
                                </div>

                                <div class="d-flex flex-column align-items-center flex-md-row justify-content-md-center">
                                    <button class="rounded-btn btn-secondary rounded rounded-3 me-0 me-md-3 mb-2 mb-md-0"
                                    @click="openModifyCardModal(card)">Modify</button>
                                    <button class="rounded-btn btn-danger rounded rounded-3" @click="deleteCard(card.id)">Delete</button>
                                </div>
                                <div v-if="isCardReserved(card.id)">
                                    <hr>
                                    <p>User: {{ whoIsCardConnectedTo(card.id)}}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div v-else>
                <div class="alert alert-success rounded rounded-3" role="alert">
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
                                    <button class="btn btn-secondary rounded rounded-3 me-3" @click="openModifyCardModal(card)">Modify</button>
                                    <button class="btn btn-danger rounded rounded-3" @click="deleteCard(card.id)">Delete Card</button>
                                    <i class="fa fa-plus-circle"></i>
                                </div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <transition name="fade">
        <div v-show="showModifyCardModal" class="modal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered modal-lg">
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
                <div class="modal-footer text-center">
                    <button type="button" class="btn btn-secondary mx-auto" @click="closeModifyCardModal">Close</button>
                    <button type="submit" class="btn btn-primary mx-auto">Modify Card</button>
                </div>
                </form>
            </div>
            </div>
        </div>
        </transition>

        <transition name="fade">
        <div v-show="showConnectModal" class="modal" tabindex="-1">
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
                        <option disabled value="">Select a user</option>
                        <option v-for="user in unassignedUsers" :key="user.id" :value="user.id">
                        {{ user.name }}
                        </option>
                    </select>
                    </div>
                </div>
                <div class="modal-footer text-center">
                    <button type="button" class="btn btn-secondary mx-auto" @click="closeConnectModal">Close</button>
                    <button type="submit" class="btn btn-primary mx-auto">Connect Card</button>
                </div>
                </form>
            </div>
            </div>
        </div>
        </transition>
    </div>
</template>

<script setup>
    import axios from "axios";
    import { ref, computed, watchEffect } from "vue";

    const header =
    {
        headers:
        { "Authorization": "Bearer " + localStorage.getItem("access_token") }
    };

    const msg = ref("");
    const users = ref([]);
    const cards = ref([]);
    const userCards = ref([]);
    const cardNumber = ref("");
    const showInfo = ref(false);
    const selectedUserId = ref("");
    const unassignedUsers = ref([]);
    const selectedCardId = ref(null);
    const showModifyCardModal = ref(false);

    const showConnectModal = ref(false);
    const showDisconnectModal = ref(false);
    const selectedCardIdForConnect = ref(null);
    const selectedCardIdForDisconnect = ref(null);

    const fetchCards = async () =>
    {
        const response = await axios.get("http://127.0.0.1:5000/cards", header)
        .then((response) =>
        {
            msg.value = "ACTIVE CARDS"
            cards.value = response.data;
        })
        .catch((error) =>
        {
            if (error.response.status === 404)
            {
                cards.value = []
                msg.value = "CARDS NOT FOUND"
            }
            else alert(error);
        });
    };

    const fetchUsers = async () =>
    {
        const response = await axios.get("http://127.0.0.1:5000/users", header);
        users.value = response.data;
    };

    const fetchUserCards = async () =>
    {
        const response = await axios.get("http://127.0.0.1:5000/user_cards", header).
        then((response) => {userCards.value = response.data; })
        .catch((error) => {})
    };

    watchEffect(async () =>
    {
        await fetchUsers();
        await fetchCards();
        await fetchUserCards();
    });


    watchEffect(() =>
    {
        if (userCards.value.length > 0 && users.value.length > 0) checkUserAssignment();
        else if (users.value.length > 0)
        {
            users.value.forEach((user) =>
            { unassignedUsers.value.push(user); });
        }
    });

    const isCardReserved = (cardId) =>
    { return userCards.value.some((userCard) => userCard.card_id === cardId); };

    const sortedCards = computed(() =>
    { return cards.value.slice().sort((a, b) => a.id - b.id); });

    const whoIsCardConnectedTo = (cardid) =>
    {
        const usercard_user_id = userCards.value.find((userCard) => userCard.card_id === cardid).user_id;
        const user = users.value.find((user) => user.id === usercard_user_id);
        return user.name;
    };

    const openModifyCardModal = (card) =>
    {
        selectedCardId.value = card.id;
        showModifyCardModal.value = true;
        cardNumber.value = card.card_number;
    };

    const closeModifyCardModal = () =>
    { showModifyCardModal.value = false; };

    const openConnectModal = (cardId) =>
    {
        showConnectModal.value = true;
        selectedCardIdForConnect.value = cardId;
    };

    const closeConnectModal = () =>
    { showConnectModal.value = false; };

    const modifyCard = async () =>
    {
        const data =
        { card_number: cardNumber.value, };

        const response = await axios.patch(`http://127.0.0.1:5000/cards/${selectedCardId.value}`, data, header);

        await fetchCards();
        closeModifyCardModal();
    };

    const deleteCard = async (id) =>
    {
        const userCard = userCards.value.find((uc) => uc.card_id === id);

        if (userCard)
        {
            alert("This card is currently connected to a user. Please disconnect it before deleting.");
            return;
        }

        const response = await axios.delete(`http://127.0.0.1:5000/cards/${id}`, header);
        await fetchCards();
    };


    const connectCardToUser = async (userId) =>
    {
        const response = await axios.post(`http://127.0.0.1:5000/user_cards`,
        {
            card_id: selectedCardIdForConnect.value,
            user_id: userId,
        }, header);

        await fetchUserCards();
        closeConnectModal();
    };

    const disconnectCardFromUser = async (cardid) =>
    {
        const del_userCard = userCards.value.find((uc) => uc.card_id === cardid);
        const response = await axios.delete(`http://127.0.0.1:5000/user_cards/${del_userCard.id}`, header);

        location.reload();
        await fetchUserCards();
    };

    const checkUserAssignment = () =>
    {
        unassignedUsers.value = [];

        if (userCards.value.length === 0)
        {
            users.value.forEach((user) =>
            { unassignedUsers.value.push(user); });
        }
        else
        {
            users.value.forEach((user) =>
            {
                const userCard = userCards.value.find((uc) => uc.user_id === user.id);
                if (!userCard) unassignedUsers.value.push(user);
            });
        }
    };
</script>

<style scoped>
    .modal
    {
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 9999;
        display: flex;
        position: fixed;
        font-weight: bold;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .alert
    {
        border-radius: 2rem;
        box-shadow: 0 5px 5px 5px rgba(0, 0, 0, 0.2);
    }
    .alert-success
    {
        color: #fff;
        border-color: #008000;
        background-color: rgba(0, 196, 0, 0.3);
    }

    .alert-danger
    {
        color: #fff;
        border-color: #cb0b01;
        background-color: rgba(203, 11, 1, 0.30);
    }

    .card
    {
        color: #fff;
        padding: 1rem 0;
        font-weight: bold;
        border-radius: 2rem;
        background-color: #413a63;
        box-shadow: 0 5px 5px 5px rgba(0, 0, 0, 0.2);
    }
    .card p { color:#fff; }
    .fade-enter-from, .fade-leave-to { opacity: 0; }
    .fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
</style>