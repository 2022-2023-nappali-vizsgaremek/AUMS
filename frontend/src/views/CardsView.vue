<template>
    <div class="container text-center pt-5 mt-5">
        <div>
            <Cards ref="activeCardsComponent" />
        </div>
        <hr/>
        <div>
            <UnknownCards @cardActivated="updateActiveCards" />
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue";
import Cards from "../components/Cards.vue";
import UnknownCards from "../components/UnknownCards.vue";

const activeCardsComponent = ref(null);

const updateActiveCards = () =>
{ if (activeCardsComponent.value) activeCardsComponent.value.fetchCards(); };
</script>