<template>
  <div class="my-3 mx-5 center-select">
    <select
      class="form-select select-custom"
      id="userSelect"
      v-model="selectedUserId" 
      required @change="loadEventsByUser(selectedUserId)">
      <option disabled value="">Please select a user</option>
      <option v-for="user in users.value" :key="user.id" :value="user.id">
        {{ user.name }}
      </option>
    </select>
  </div>
  <div class="navigatorIconContainer ms-2 mb-2 text-center">
  <i v-if="isNavigatorVisible" class="fa fa-angle-double-left" aria-hidden="true" type="button" @click="toggleNavigator"></i>
  <i v-else class="fa fa-angle-double-right" aria-hidden="true" type="button" @click="toggleNavigator"></i>
  </div>
  <div class="wrap">
      <div :class="{ 'nav-hidden': !isNavigatorVisible }" class="nav-container">
        <DayPilotNavigator id="nav" :config="navigatorConfig" />
      </div>
        <div :class="{ 'content-expanded': !isNavigatorVisible }" class="content" hidden>
        <DayPilotCalendar id="dp" :config="config" ref="calendar" />
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
</template>
  
<script>
    const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };

  import {DayPilot, DayPilotCalendar, DayPilotNavigator} from '@daypilot/daypilot-lite-vue';
  import { ref } from 'vue';
  import axios from 'axios';


  export default {
    name: 'Calendar',

    data: function() {

      const users = ref([]);
      var date = (new Date()).toISOString().split('T')[0];
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
      

      return {
        users,
        selectedUserId,
        info,
        date,
        modalActive,
        closeModal,
        openModal,
        isNavigatorVisible,
        toggleNavigator,
        events: [],
        navigatorConfig: {
            showMonths: 3,
            skipMonths: 3,
            selectMode: "Week",
            startDate: date,
            selectionDay: date,
            onTimeRangeSelected: args => {
              this.config.startDate = args.day;
            }
        },
        config: {
          viewType: "Week",
          startDate: date,
          durationBarVisible: true,
          eventDeleteHandling: "Disabled",
          eventMoveHandling: "Disabled",
          eventResizeHandling: "Enabled",
          eventHoverHandling: "Disabled",
          eventClickHandling: "Enabled",
          eventClickHandling: "Bubble",
          onEventClick: args => {
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
          }
        }
      }
    },
    components: {
      DayPilotCalendar,
      DayPilotNavigator,
    },
    computed: {
      calendar() {
        return this.$refs.calendar.control;
      }
    },
    methods: {
      watchCalendarHeight() {
        setInterval(() => {
          const calendarElement = document.querySelector('#dp > div:nth-child(2)');
          if (calendarElement && calendarElement.style.height !== '100%') {
            calendarElement.style.height = '100%';
          }
        }, 500);
      },
      async loadUsers() {
        const response = await axios.get('http://127.0.0.1:5000/users', header);
        this.users.value = response.data;
      },
      adjustCalendarHeight() {
        const calendarElement = document.querySelector('#dp > div:nth-child(2)');
        if (calendarElement) {
          calendarElement.style.height = 'calc(100% - 30px)';
        }
      },
      async loadEventsByUser(userid) {
        let events = [];
        const response = await axios.get('http://127.0.0.1:5000/schedule', header);
        const raw_events = response.data;
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

        for (const event of raw_events) {
          if (event.user_id == userid) {
            let color = colors[Math.floor(Math.random() * colors.length) + 1];
            events.push({
              id: event.id,
              start: event.start,
              end: event.end,
              backColor: color
            });
          }
        }
        this.calendar.update({events});
        document.querySelector('.content').hidden = false;
      },
    },
    mounted() {
      this.loadUsers();
      this.watchCalendarHeight();
    }
  }
</script>
  
<style>
  body{
    background: #9053c7;
    background: -webkit-linear-gradient(-135deg, #c850c0, #4158d0);
    background: -o-linear-gradient(-135deg, #c850c0, #4158d0);
    background: -moz-linear-gradient(-135deg, #c850c0, #4158d0);
    background: linear-gradient(-135deg, #c850c0, #4158d0);
  }

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
  
  .left {
    margin-right: 10px;
  }
  
  .content {
    transition: all 0.5s ease;
    width: calc(100% - 20px);
    height: 100%;
  }

  .content-expanded {
    width: 100%;
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

  .select-custom {
    font-family: Poppins-Regular;
    font-size: 15px;
    line-height: 1.5;
    color: #666666;
    display: block;
    width: 50%;
    background: #e6e6e6;
    height: 50px;
    border-radius: 25px;
    padding: 0 30px;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
  }

  .select-custom:focus {
    outline: none;
    box-shadow: 0 0 10px rgba(87, 184, 70, 0.5);
  }

  .select-custom::-ms-expand {
    display: none;
  }

  .select-custom:hover {
    cursor: pointer;
  }

  .center-select {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .nav-wrapper {
    display: flex;
  }

  .arrow-container {
    display: flex;
    align-items: center;
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
    margin-left: -212px;
  }

  .navigatorIconContainer{
    width: 35px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
  }
</style>