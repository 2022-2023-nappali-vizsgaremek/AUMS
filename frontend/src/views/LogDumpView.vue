<template>
    <div class="container-fluid mt-5 pt-5">
        <div class="text-white text-center mb-5">
            <h1>Log Viewer</h1>
            <p class="text-white">
                This page shows the logs of the backend server. The logs are fetched
                from the server every 5 seconds.
            </p>
        </div>
        <div class="table-responsive">
            <table
            class="table table-hover shadow border border-light
            table-bordered bg-transparent rounded rounded-3 overflow-hidden">
                <thead>
                    <tr class="align-middle text-center bg-dark text-light bg-opacity-75">
                        <th role="button" @click="toggleSort('timestamp')">
                            <span class="nowrap">
                                TIME
                                <i v-if="sortBy.field === 'timestamp'"
                                    :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fa fa-sort"></i>
                            </span>
                        </th>
                        <th role="button" @click="toggleSort('level')">
                            <span class="nowrap">
                                LEVEL
                                <i v-if="sortBy.field === 'level'"
                                    :class="sortBy.order === 'asc' ? 'fa fa-sort-asc' : 'fa fa-sort-desc'"></i>
                                <i v-else class="fa fa-sort"></i>
                            </span>
                        </th>
                        <th>MESSAGE</th>
                    </tr>
                </thead>
                <tbody>
                    <tr
                        v-for="(log, index) in sortedLogs"
                        :key="index"
                        :class="{
                        'log-warning': log.level === 'WARNING',
                        'log-error': log.level === 'ERROR',
                        'log-info': log.level === 'INFO', }">

                        <td>{{ log.timestamp }}</td>
                        <td>{{ log.level }}</td>
                        <td>{{ log.message }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import axios from "axios";
import { useSorting } from "../assets/sorting";
import { ref, onMounted, onUnmounted, computed } from "vue";

const logs = ref([]);
const { sortBy, toggleSort, sortData } = useSorting();

const header =
{
    headers:
    { Authorization: "Bearer " + localStorage.getItem("access_token"), },
};

const fetchLogs = async () =>
{
    try
    {
        const response = await axios.get("http://127.0.0.1:5000/log_dump", header);
        logs.value = parseLogs(response.data.log_dump);
    }
    catch (error)
    { alert("Failed to fetch logs"); }
};

const parseLogs = (logData) =>
{
    const logs = [];
    const logLines = logData.split("\n");

    logLines.forEach((line) =>
    {
        const matches = line.match(/\(([^)]+)\) (\w+): (.+)/);

        if (matches)
        {
            if (!matches[3].includes("dump"))
            {
                logs.push(
                {
                    level: matches[2],
                    message: matches[3],
                    timestamp: matches[1],
                });
            }
        }
    });

    return logs;
};

const sortedLogs = computed(() =>
{ return sortData(logs.value, sortBy.value); });

let intervalId;
onMounted(() =>
{
    fetchLogs();
    intervalId = setInterval(fetchLogs, 5000);
});

onUnmounted(() => { clearInterval(intervalId); });
</script>

<style scoped>
    .log-warning { background-color: #f0ad4e; }
    .log-error { background-color: #d9534f; }
    .log-info { background-color: #2bacd469; }

    .table tbody tr td:nth-child(2) { font-weight: bold; }
    .table tbody tr td:last-child { word-break: break-word; }
    .table tbody tr td:nth-child(1),  .table tbody tr td:nth-child(2) { text-align: center; }
</style>