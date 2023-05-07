import { reactive } from "vue";

export function useSorting() {
  const sortBy = reactive({ field: "", order: "asc" });

  function toggleSort(field) {
    if (sortBy.field === field) {
      sortBy.order = sortBy.order === "asc" ? "desc" : "asc";
    } else {
      sortBy.field = field;
      sortBy.order = "asc";
    }
  }

  function sortData(data) {
    if (sortBy.field !== "") {
      data.sort((a, b) => {
        if (a[sortBy.field] < b[sortBy.field]) return sortBy.order === "asc" ? -1 : 1;
        if (a[sortBy.field] > b[sortBy.field]) return sortBy.order === "asc" ? 1 : -1;
        return 0;
      });
    }
    return data;
  }

  return { sortBy, toggleSort, sortData };
}
