<template>
  <div class="container-fluid">
    <div class="row justify-content-center">
      <div class="col-12 mt-5 text-center">
        <select
          class="form-select mt-5 shadow mb-3 rounded rounded-3 p-3 text-center w-50 mx-auto fs-5"
          id="userSelect"
          v-model="selectedUserId" 
          required @change="loadEventsByUser(selectedUserId)">
          <option disabled value="">Please select a user</option>
          <option v-for="user in users.value" :key="user.id" :value="user.id">
            {{ user.name }}
          </option>
        </select>
      </div>
    </div>
    <div class="row justify-content-center mt-3 mb-3">
      <div class="col-12 text-center">
        <div class="navigatorIconContainer">
          <i v-if="isNavigatorVisible" class="fa fa-angle-double-left" aria-hidden="true" type="button" @click="toggleNavigator"></i>
          <i v-else class="fa fa-angle-double-right" aria-hidden="true" type="button" @click="toggleNavigator"></i>
        </div>
      </div>
    </div>
    <div class="row justify-content-center">
      <div class="col-12">
        <div class="wrap">
          <div :class="{ 'nav-hidden': !isNavigatorVisible }" class="nav-container">
            <DayPilotNavigator id="nav" :config="navigatorConfig" />
          </div>
          <div :class="{ 'content-expanded': !isNavigatorVisible }" class="content ms-4 me-3 mb-5" hidden>
            <DayPilotCalendar id="dp" :config="config" ref="calendar" />
          </div>
        </div>
      </div>
    </div>

    <div v-if="modalActive" class="modal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Daily Schedule Information</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <p v-for="inf in info">{{ inf }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="closeModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive, watch, nextTick } from 'vue'; // Add nextTick import here

  import axios from 'axios';
  import {
    DayPilot,
    DayPilotCalendar,
    DayPilotNavigator,
  } from '@daypilot/daypilot-lite-vue';

  const header = {
    headers: {
      Authorization: 'Bearer ' + localStorage.getItem('access_token'),
    },
  };

  const users = reactive([]);
  let date = new Date().toISOString().split('T')[0];
  const info = ref('');
  const modalActive = ref(false);
  const selectedUserId = ref('');
  const isNavigatorVisible = ref(false);

  const openModal = (resp) => {
    modalActive.value = true;
    info.value = resp;
  };

  const closeModal = () => {
    modalActive.value = false;
  };

  const toggleNavigator = () => {
    isNavigatorVisible.value = !isNavigatorVisible.value;
  };

  const loadUsers = async () => {
    const response = await axios.get('http://127.0.0.1:5000/users', header);

    users.value = response.data;
    users.value = users.value.filter((user) => user.id !== 1);
    users.value = users.value.filter((user) => user.id !== 2);
  };

    
        let colors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		                  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
                      '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
                      '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
                      '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
                      '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
                      '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
                      '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
                      '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
                      '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'];
                      
const loadEventsByUser = async (userid) => {
  var events = [];
  const response = await axios
    .get('http://127.0.0.1:5000/schedule', header)
    .catch((error) => {
      if (error.response.status == 404) {
        alert('No schedule found for this user');
      }
    });

  const raw_events = response.data;

  for (const event of raw_events) {
    if (event.user_id == userid && event.end !== null) {
      let color = colors[Math.floor(Math.random() * colors.length) + 1];
      events.push({
  id: event.id,
  start: new DayPilot.Date(event.start),
  end: new DayPilot.Date(event.end),
  backColor: color,
  textColor: "white",
}
);
      
    }
  }


config.events = events;
config.startDate = new Date(config.startDate).toISOString(); // Force a re-render
document.querySelector('.content').hidden = false;



};




  const watchCalendarHeight = () => {
    setInterval(() => {
      const calendarElement = document.querySelector('#dp > div:nth-child(2)');
      if (calendarElement && calendarElement.style.height !== '100%') {
        calendarElement.style.height = '100%';
      }
    }, 500);
  };

  const calendar = ref(null);
  watch(calendar, () => {
    if (calendar.value) {
      loadUsers();
      watchCalendarHeight();
    }
  });

  const navigatorConfig = {
    showMonths: 3,
    skipMonths: 3,
    selectMode: 'Week',
    startDate: date,
    selectionDay: date,
    onTimeRangeSelected: (args) => {
      config.startDate = args.day;
    },
  };

  const config = reactive({
    viewType: 'Week',
    startDate: date,
    durationBarVisible: true,
    eventDeleteHandling: 'Disabled',
    eventMoveHandling: 'Disabled',
    eventResizeHandling: 'Enabled',
    eventHoverHandling: 'Disabled',
    eventClickHandling: 'Enabled',
    eventClickHandling: 'Bubble',
    events: [], // Add this line
    onEventClick: (args) => {
      let resp = [];
      for (const arg in args.e.data) {
        if (arg == 'start') {
                resp.push('date: ' + args.e.data[arg].toString().split('T')[0] + '\n');
    }
    if (arg == 'start' || arg == 'end') {
      resp.push(arg + ': ' + args.e.data[arg].toString().split('T')[1]);
    }
  }
  openModal(resp);
},
});
</script>


<style>


  #dp {
    height: 100%;
  }

  #dp:nth-child(2){
    height: 100% !important;
  }

  .calendar_default_main::after{
    height: 100%;
  }

  .wrap {
    display: flex;
    height: 100%;
  }
  



  .calendar_default_event_inner {
    background: #2e78d6;
    color: white;
    border-radius: 5px;
    opacity: 0.9;
  }

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





  .fa-angle-double-left{
    font-size: 2rem;
    color: #fff;
  }

  .fa-angle-double-right{
    font-size: 2rem;
    color: #fff;
  }

  .nav-container {
    transition: all 0.5s;
  }

  .nav-hidden {
    margin-left: -225px;
  }


</style>