
import Signup from '../Signup/Signup.vue'
import ConfirmPayment from '../ConfirmPayment/ConfirmPayment.vue'
import Status from '../Status/Status.vue'
export default {
  name: "ReservationProcess",
  data: function () {
    return {
      progress: 0,
      complated: false
    };
  },
  components: {
    'sign-up': Signup,
    'confirm-payment': ConfirmPayment,
    'reservation-status': Status
  },
  computed: {
    lang() {
      return this.$store.getters.lang;
    },
    reservationStep(){
      if(this.$store.getters.isLoggedIn){
        const step = JSON.parse(localStorage.getItem('auth'));
        this.progress = 2 //step.current_step || 1;
      }else{
        this.progress = 1;
      }
      return this.progress;
    },
    isRoomNotSaved(){
      return (localStorage.getItem('room') != null);
    },
    isRoomReserved(){
      const user = JSON.parse(localStorage.getItem('auth'))
      if(user){
        const isReserved = user.reservarion_id
        return isReserved? true : false
      }
      return false
    }
  },
  methods:{
    loadroom(){
      if(this.$store.getters.isLoggedIn){
        const user = JSON.parse(localStorage.getItem('auth'))
        const isReserved = user.reservarion_id
        if(isReserved == null && !!localStorage.getItem('room')){
          const savedRoom = JSON.parse(localStorage.getItem('room'))
          this.$store.dispatch('reserveRoom', savedRoom.room.id)
          .then(response => {
            //this.$store.dispatch('fetchReservation');
          })
        }else{
          this.$store.dispatch('fetchReservation', isReserved);
        }
      }
    }
  },
  mounted(){
    this.loadroom();
  }
};