<template>
  <main class="flex flex-col justify-center items-center w-full h-full">
    <form
      @submit.prevent="authorization"
      class="flex flex-col gap-5 p-6 rounded-md border showDownAnim"
    >
      <p class="text-2xl text-center">Авторизация в систему</p>
      <div class="flex flex-col gap-3">
        <vInput placeholder="Логин" v-model="user.login" required />
        <vInput
          placeholder="Пароль"
          type="password"
          v-model="user.password"
          required
        />
        <div class="text-center text-red-400 rounded-md">
          {{ errMessage }}
        </div>
      </div>
      <vButton :type="loading ? 'loading' : 'success'">
        <div class="text-xl i-tabler:user" />
        <p class="text-lg">Войти</p>
      </vButton>
    </form>
  </main>
</template>

<script setup>
// Import libs
import { ref, onMounted } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
// Import components
import vButton from "../components/v-button.vue";
import vInput from "../components/v-input.vue";
import router from "../router/index.js";

const user = ref({
  login: undefined,
  password: undefined,
});

const loading = ref(false);
const errMessage = ref();
const ip = "http://127.0.0.1:8000";

function authorization() {
  loading.value = true;
  axios
    .post(
      `${ip}/teacher/auth?email=${user.value.login}&password=${user.value.password}`
    )
    .then((res) => {
      Cookies.set("userInfo", JSON.stringify(res.data.response));
      router.push("/app");
    })
    .catch(() => {
      errMessage.value = 'Неверный логин или пароль.';
      loading.value = false;
    });
}
</script>
