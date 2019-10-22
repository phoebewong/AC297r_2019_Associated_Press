Vue.config.devtools = true;
var vue = new Vue({
  el: "#app",
  data () {
    return {
      pending: false,
      error: null,
      title: "",
      body: "",
      tags: [],
      images: []
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
          this.tags = response.body.data.tags;
          this.images = response.body.data.images;
        }
        this.pending = false;
      }, response => {
        console.log("match fetch error", response);
        this.error = response.status;
        this.pending = false;
      });
    },
    makeImgSource(img_id){
      return 'static/img/thumbnail/' + img_id + '.jpg'
    }
  },
  computed: {},
  filters: {}
});
