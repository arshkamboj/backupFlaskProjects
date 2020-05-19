<template>
    <div class="container">
        <div class="row">
            <div class="col-md-6 mt-5 mx-auto">
                <form v-on:submit.prevent="updateProfile">
                    <h1 class="h3 mb-3 font-weight-normal">Update Profile</h1>
                    <div class="form-group">
                        <label for="first_name">First Name</label>
                        <input type="text" v-model="first_name" class="form-control" name="first_name" placeholder="Enter First Name">
                    </div>
                    <div class="form-group">
                        <label for="last_name">Last Name</label>
                        <input type="text" v-model="last_name" class="form-control" name="last_name" placeholder="Enter Last Name">
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" v-model="email" class="form-control" name="email" placeholder="Enter Email">
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" v-model="password" class="form-control" name="password" placeholder="Enter Password">
                    </div>
                    <div class="form-group">
                          <label>Upload Profile Image</label>
                            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
                            <button v-on:click="submitFile()">Upload</button>
                     </div>
                    <button class="btn btn-lg btn-primary btn-block">Update Profile</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import router from '../router'

export default {
  data () {
    return {
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      file: ''
    }
  },

  methods: {
    updateProfile () {
      let formData = new FormData()
      formData.append('file', this.file)

      axios.post('users/updateProfile', {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        password: this.password,
        formData: {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      }).then(res => {
        router.push({ name: 'Profile' })
      }).catch(err => {
        console.log(err)
      })
    },

    handleFileUpload () {
      this.file = this.$refs.file.files[0]
    }
  }
}

</script>
