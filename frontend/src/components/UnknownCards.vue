<template>
    <div class="row">
        <div class="col my-4 mx-5">
            <div v-if="unknownCards.length < 1" class="alert alert-danger rounded rounded-3" role="alert">
                <h1>CARDS NOT FOUND</h1>
            </div>
            <div v-else-if="sortedCards.length <= 9">
                <div class="alert alert-success rounded rounded-3" role="alert">
                    <h1>INACTIVE CARDS</h1>
                </div>
                <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
                    <div v-for="unknownCard in unknownCards" :key="unknownCard.id" class="col">
                        <div class="card rounded rounded-3">
                            <div class="card-body">
                                <h5 class="card-title text-white">Id: {{ unknownCard.id }}</h5>
                                <p class="card-text text-white">Card number: {{ unknownCard.card_number }}</p>
                                <div class="d-flex flex-column align-items-center flex-md-row justify-content-md-center">
                                    <button class="rounded-btn btn-success rounded rounded-3 me-0 me-md-3 mb-2 mb-md-0" @click="activateCard(unknownCard.id)">Activate</button>
                                    <button class="rounded-btn btn-danger rounded rounded-3" @click="deleteUnknownCard(unknownCard.id)">Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else>
                <div class="alert alert-success rounded rounded-3" role="alert">
                    <h1>INACTIVE CARDS</h1>
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
                            <button class="btn btn-success rounded rounded-3 me-3" @click="activateCard(unknownCard.id)">Activate</button>
                            <button class="btn btn-danger rounded rounded-3" @click="deleteUnknownCard(unknownCard.id)">Delete Card</button>
                        </div>
                        </div>
                    </li>
                    </ul>
                </div>
            </div>
        </div>
        <button class="login-form-btn btn-outline-success rounded mx-auto rounded-3 my-4 w-100" @click="openAddCardModal">Add Card</button>

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
                    <div class="modal-footer text-center">
                        <button type="button" class="btn btn-secondary mx-auto " @click="closeAddCardModal">Close</button>
                        <button type="submit" class="btn btn-success mx-auto ">Add Card</button>
                    </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import axios from "axios";
    import { ref, computed } from "vue";


    const header =
    {
        headers:
        { "Authorization": "Bearer " + localStorage.getItem("access_token") }
    };

    const unknownCards = ref([]);
    const newCardNumber = ref("");
    const showAddCardModal = ref(false);

    const fetchUnknownCards = async () =>
    {
        try
        {
            const response = await axios.get("http://127.0.0.1:5000/unknown_cards", header);
            unknownCards.value = response.data;
        }
        catch (error)
        {
            if (error.response.status === 404) unknownCards.value = [];
            else alert(error)
        }
    };

    const sortedCards = computed(() =>
    { return unknownCards.value.slice().sort((a, b) => a.id - b.id); });

    const openAddCardModal = () =>
    { showAddCardModal.value = true; };

    const closeAddCardModal = () =>
    { showAddCardModal.value = false; };

    const addUnknownCard = async () =>
    {
        uk_card_number: newCardNumber.value;

        const response = await axios.post(`http://127.0.0.1:5000/card_validation/${newCardNumber.value}`, {}, header)
        .catch((error) => { if (error.response.status == 409) alert(error.response.data.message) })
        .then((response) =>
        {
            if (response == undefined) return alert("Card already exists")
            else if (response.status == 200) alert("Card added successfully")
        });

        await fetchUnknownCards();
        closeAddCardModal();
    };

    const deleteUnknownCard = async (id) =>
    {
        const response = await axios.delete(`http://127.0.0.1:5000/unknown_cards/${id}`, header)
        .catch((error) => { if (error.response.status == 404) alert(error.response.data.message) });

        await fetchUnknownCards();
    };

    const activateCard = async (id) =>
    {
        const response = await axios.post(`http://127.0.0.1:5000/activate_card/${id}`, {}, header);
        location.reload();

        await fetchUnknownCards();
    };

    fetchUnknownCards();
</script>

<style scoped>
    .modal
    {
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        position: fixed;
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
        border-color: #808080;
        background-color: rgba(128, 128, 128, 0.50);
    }
    .alert-danger
    {
        color: #fff;
        border-color: #cb0b01;
        background-color: rgba(203, 11, 1, 0.30);
    }

    .card
    {
        padding: 1rem 0;
        font-weight: bold;
        border-radius: 2rem;
        background-color: #413a63;
        box-shadow: 0 5px 5px 5px rgba(0, 0, 0, 0.2);
    }
</style>