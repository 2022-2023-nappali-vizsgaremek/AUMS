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
          }}}}};

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
  