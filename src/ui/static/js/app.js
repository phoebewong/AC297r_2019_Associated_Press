Vue.config.devtools = true;
var vue = new Vue({
  el: "#app",
  data () {
    return {
      pending: false,
      error: null,
      title: "",
      body: "",
      matches: []
    }
  },
  async created () {
    console.log("created");
  },
  methods: {
    getMatches () {
      console.log("fetching matches");
      this.pending = true;
      var data = { title: this.title, body: this.body };
      this.$http.post("/match", data).then(response => {
        if (response.body.status == "ok") {
          this.matches = response.body.data;
        }
        this.pending = false;
      }, response => {
        console.log("match fetch error", response);
        this.error = response.status;
        this.pending = false;
      });
    }
  },
  computed: {},
  filters: {}
});