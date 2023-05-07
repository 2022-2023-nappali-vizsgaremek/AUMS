<template>
    <div class="container mt-5 pt-5">
        <div class="text-white text-center">
            <h1>Log Viewer</h1>
            <p class="text-white">This page shows the logs of the backend server. The logs are fetched from the server every 5 seconds.</p>
        </div>
        <div class="table-responsive">
            <table class="table table-bordered table-hover bg-white rounded rounded-4 overflow-hidden">
                <thead>
                    <tr class="align-middle text-center">
                        <th role="button" @click="toggleSort('timestamp')">
                            <span class="nowrap">
                                Time
                                <i v-if="sortBy.field === 'timestamp'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fa fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('level')">
                            <span class="nowrap">
                                Level
                                <i v-if="sortBy.field === 'level'" :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fa fa-sort"></i>
                            </span>
                        </th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(log, index) in sortedLogs" :key="index" :class="{'log-warning': log.level === 'WARNING', 'log-error': log.level === 'ERROR', 'log-info': log.level === 'INFO'}">
                        <td>{{ log.timestamp }}</td>
                        <td>{{ log.level }}</td>
                        <td>{{ log.message }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
  
  <script>
  import { ref, onMounted, onUnmounted, computed } from "vue";
  import sorting from "../assets/sorting";
  import axios from "axios";
  
  export default {
    mixins: [sorting],
    computed: {
      sortedLogs() {
        return this.sortData([...this.logs]);
      },
    },
    setup() {
      const logs = ref([]);

      const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };
  
      const fetchLogs = async () => {
        try {
          const response = await axios.get("http://127.0.0.1:5000/log_dump", header);
          logs.value = parseLogs(response.data.log_dump);
        } catch (error) {
          console.error("Error fetching logs:", error);
        }
      };
  
      const parseLogs = (logData) => {
        const logLines = logData.split('\n');
        const logs = [];

        logLines.forEach((line) => {
            const matches = line.match(/\(([^)]+)\) (\w+): (.+)/);

            if (matches) {
                if (!matches[3].includes('dump')) {
                    logs.push({
                        timestamp: matches[1],
                        level: matches[2],
                        message: matches[3],
                    });
                }


            }
        });

        return logs;
    };

    let intervalId;
  
    onMounted(() => {
        fetchLogs();
        intervalId = setInterval(fetchLogs, 5000);
    });

    onUnmounted(() => {
        clearInterval(intervalId);
    });
  
      return { logs };
    },
  };
  </script>

<style scoped>
    .log-warning  {
        background-color: #f0ad4e;
    }

    .log-error {
        background-color: #d9534f;
    }

    .log-info {
        background-color: #2bacd4;
    }

    .table tbody tr td:nth-child(2){
        font-weight: bold;
    }

    .table tbody tr td:nth-child(1), .table tbody tr td:nth-child(2){
        text-align: center;
    }

    .table tbody tr td:last-child {
        word-break: break-word;
    }
</style>
  