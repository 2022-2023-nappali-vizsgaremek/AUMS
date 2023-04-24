<template>
    <div class="wrap">
      <div class="left">
        <DayPilotNavigator id="nav" :config="navigatorConfig" />
      </div>
      <div class="content">
        <DayPilotCalendar id="dp" :config="config" ref="calendar" />
      </div>
    </div>
  </template>
  
  <script>
  import {DayPilot, DayPilotCalendar, DayPilotNavigator} from '@daypilot/daypilot-lite-vue'
  
  export default {
    name: 'Calendar',
    data: function() {
      return {
        events: [],
        navigatorConfig: {
          showMonths: 3,
          skipMonths: 3,
          selectMode: "Week",
          startDate: "2022-03-01",
          selectionDay: "2022-02-28",
          onTimeRangeSelected: args => {
            this.config.startDate = args.day;
          }
        },
        config: {
          viewType: "Week",
          startDate: "2022-02-28",
          durationBarVisible: false,
          timeRangeSelectedHandling: "Enabled",
          onTimeRangeSelected: async (args) => {
            const modal = await DayPilot.Modal.prompt("Create a new event:", "Event 1");
            const dp = args.control;
            dp.clearSelection();
            if (modal.canceled) {
              return;
            }
            dp.events.add({
              start: args.start,
              end: args.end,
              id: DayPilot.guid(),
              text: modal.result
            });
          },
          eventDeleteHandling: "Disabled",
          onEventMoved: () => {
            console.log("Event moved");
          },
          onEventResized: () => {
            console.log("Event resized");
          },
        },
      }
    },
    components: {
      DayPilotCalendar,
      DayPilotNavigator
    },
    computed: {
      // DayPilot.Calendar object - https://api.daypilot.org/daypilot-calendar-class/
      calendar() {
        return this.$refs.calendar.control;
      }
    },
    methods: {
      loadEvents() {
        // placeholder for an HTTP call
        const events = [
          {
            id: 1,
            start: "2022-02-28T10:00:00",
            end: "2022-02-28T11:00:00",
            text: "Event 1",
            backColor: "#6aa84f",
            borderColor: "#38761d",
          },
          {
            id: 2,
            start: "2022-02-28T13:00:00",
            end: "2022-02-28T16:00:00",
            text: "Event 2",
            backColor: "#f1c232",
            borderColor: "#bf9000",
          },
          {
            id: 3,
            start: "2022-03-01T13:30:00",
            end: "2022-03-01T16:30:00",
            text: "Event 3",
            backColor: "#cc4125",
            borderColor: "#990000",
          },
          {
            id: 4,
            start: "2022-03-01T10:30:00",
            end: "2022-03-01T12:30:00",
            text: "Event 4"
          },
        ];
        this.calendar.update({events});
      },
    },
    mounted() {
      this.loadEvents();
    }
  }
  </script>
  
  <style>
  .wrap {
    display: flex;
    background: #9053c7;
    background: -webkit-linear-gradient(-135deg, #c850c0, #4158d0);
    background: -o-linear-gradient(-135deg, #c850c0, #4158d0);
    background: -moz-linear-gradient(-135deg, #c850c0, #4158d0);
    background: linear-gradient(-135deg, #c850c0, #4158d0);
  }
  
  .left {
    margin-right: 10px;
  }
  
  .content {
    flex-grow: 1;
  }
  
  
  .calendar_default_event_inner {
    background: #2e78d6;
    color: white;
    border-radius: 5px;
    opacity: 0.9;
  }
  </style>
  