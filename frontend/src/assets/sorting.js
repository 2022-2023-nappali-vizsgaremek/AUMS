export default {
    data() {
      return {
        sortBy: { field: '', order: 'asc' },
      };
    },
    methods: {
      toggleSort(field) {
        if (this.sortBy.field === field) {
          this.sortBy.order = this.sortBy.order === 'asc' ? 'desc' : 'asc';
        } else {
          this.sortBy.field = field;
          this.sortBy.order = 'asc';
        }
      },
      sortData(data) {
        if (this.sortBy.field !== '') {
          data.sort((a, b) => {
            if (a[this.sortBy.field] < b[this.sortBy.field]) return this.sortBy.order === 'asc' ? -1 : 1;
            if (a[this.sortBy.field] > b[this.sortBy.field]) return this.sortBy.order === 'asc' ? 1 : -1;
            return 0;
          });
        }
        return data;
      },
    },
  };
  