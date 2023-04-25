<template>
  <div class="container-gradient">
    <div class="container text-center">
      <div>
        <Cards ref="activeCardsComponent" />
      </div>
      <hr/>
      <div>
        <UnknownCards @cardActivated="updateActiveCards" />
      </div>
    </div>
  </div>
</template>
  
<script>
import Cards from '../components/Cards.vue';
import UnknownCards from '../components/UnknownCards.vue';

export default {
  components: {
    Cards,
    UnknownCards,
  },
  methods: {
    updateActiveCards() {
      this.$refs.activeCardsComponent.fetchCards();
    },
  },
};
</script>