<template>
  <div class="login-form centered-form">
    <div class="login-container">
      <h2>Login</h2>
      <form @submit.prevent="loginUser">
        <InputText v-model="user.email" placeholder="Email" type="text" required />
        <p v-if="userNotRegistered" class="error-message">User is not registered. Please register!</p>
        <InputText v-model="user.password" placeholder="Password" type="text" required />
        <p v-if="incorrectPassword" class="error-message">Please enter the correct password!</p>
        <Button label="Login" type="submit"></Button>
      </form>
      <router-link to="/register">Register</router-link>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { setAuthenticated } from '@/store';
import InputText from 'primevue/inputtext';
import Button  from 'primevue/button';

export default {
  data() {
    return {
      user: {
        email: "",
        password: ""
      },
      userNotRegistered: false, // To show error message when unregistered user tries to log in.
      incorrectPassword: false, // To show error message for incorrect password.
    };
  },
  components: {
    InputText,
    Button
  },
  methods: {
    async loginUser() {

      try {
        const response = await fetch("/api/users/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.user)
        });

        if (response.ok) {
            const responseData = await response.json();
            const userId = responseData.user_id;
            localStorage.setItem('userId', userId); // User id is set to access it across pages, on mounting.

            localStorage.setItem('userAuthenticated', 'true'); // To keep track of logged-in user.
            setAuthenticated(true);
            this.$router.push("/");
        } else {
            const responseText = await response.text();
            const message = JSON.parse(responseText)["detail"];

            if (message === "User does not exist") {
              this.userNotRegistered = true;
            }
            else if (message === "Incorrect password") {
              this.incorrectPassword = true;
            }
        }
      } catch (error) {
        console.error(error);
        alert("An error occurred.");
      }
    }
  }
};
</script>

<style scoped>

.centered-form {
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

h2 {
  font-size: 24px;
}

form {
  display: flex;
  flex-direction: column;
}

input {
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 10px;
  margin: 10px 0;
}

.error-message {
  font-size: 14px;
  color: red;
  margin-top: 0px;
}

</style>
