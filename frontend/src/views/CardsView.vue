<template>
  <div class="container-gradient">
    <div class="container">
      <Cards/>
    </div>
  </div>
</template>
  
<script>
import Cards from '../components/Cards.vue';
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