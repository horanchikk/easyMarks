<template>
  <div class="w-screen h-screen flex flex-col gap-5 items-center justify-center">
    <i class="i-line-md:loading-twotone-loop text-6xl"></i>
    <p class="text-xl text-bold font-mono showAnim">{{ waitingloop }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import router from '../router'

const waitingloop = ref("")
const text = ref(['Please wait.', 'Please wait..', 'Please wait...'])
const time = ref(0)

onMounted(() => {
  text.value.forEach((el) => {
    setTimeout(() => {
      setInterval(() => {
        waitingloop.value = el;
      }, 1500)
    }, time.value)
    time.value += 500;
  });
  router.push("/auth")
})
</script>
