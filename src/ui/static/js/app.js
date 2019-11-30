Vue.config.devtools = true;
var vue = new Vue({
  el: "#app",
  data () {
    return {
      pending: false,
      show_articles: false,
      error: null,
      id: "",
      title: "",
      body: "",
      chosen_model: "all",
      slider: 5,
      num_images: 16,
      time: null,
      tags: [],
      images: [],
      true_images: [],
      log_object: null
    }
  },
  async created () {
    console.log("created");
  },
  methods: {
    getMatches () {
      console.log("fetching matches");
      this.pending = true;
      var data = { title: this.title, body: this.body, model: this.chosen_model, slider: this.slider};
      this.$http.post("/match", data).then(response => {
        if (response.body.status == "ok") {
          this.id = response.body.data.id;
          this.title = response.body.data.title;
          this.time = response.body.data.time;
          this.body = response.body.data.body;
          this.tags = response.body.data.tags;
          this.images = response.body.data.images;
          this.articles = response.body.data.articles;
          this.true_images = response.body.data.true_images;
          if (this.chosen_model === "emb" || this.chosen_model === "knn"){
            this.show_articles = true;
          }
          else {
            this.show_articles = false;
          }
          if (this.log_object) {
            var log_obj = {title: this.title, body: this.body, model: this.chosen_model,
                           images: this.images, id: this.id, slider: this.slider};
            this.logData(log_obj);
          }
          else {
            this.log_object = {title: this.title, body: this.body, model: this.chosen_model,
                               images: this.images, id: this.id, slider: this.slider};
          }
        }
        this.pending = false;
      }, response => {
        console.log("match fetch error", response);
        this.error = response.status;
        this.pending = false;
      });
    },
    logData(data){
      console.log("logging data")
      this.$http.post("/log", this.log_object).then(response => {
        if (response.body.status == "ok") {
          this.log_object = data;
        }
      }, response => {
        console.log("logging error", response);
      });
    },
    makeImgSource(img_id, cat='preview'){
      return 'static/img/' + cat + '/' + img_id + '.jpg'
    },
    likeClicked(img){
      img.liked = !img.liked;
      if (img.liked === true) img.disliked = false;
    },
    dislikeClicked(img){
      img.disliked = !img.disliked;
      if (img.disliked === true) img.liked = false;
    }
  },
  computed: {},
  filters: {}
});
