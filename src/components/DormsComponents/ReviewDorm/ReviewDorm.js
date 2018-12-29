export default {
  name: "DormSearch",
  data: function () {
    return {
      showForm: true,
      rating: null,
      comment: '',
      loadingBtn: false
    };
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    }
  },
  methods: {
    submitReview(){
      if(this.$refs.form.validate()){
        this.loadingBtn = true
        const dormId = this.$route.params.id
        let data = {
          stars: this.rating,
          comment: this.comment
        }
        this.$store.dispatch('submitReview', {dormId, data}).then(()=>{
          let snackbar = {
            message: 'Status has been Updeated, successfully',
            color: 'success'
          }
          this.loadingBtn = false
          this.showForm = false
          this.$store.commit('updateSnackbar', snackbar)
        }).catch((err)=>{
          let snackbar = {
            message: err,
            color: 'error'
          }
          this.$store.commit('updateSnackbar', snackbar)
          this.loadingBtn = false
        })
      }
    }
  }
};