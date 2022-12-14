<template>
  <transition name="animDialog">
    <div
      class="fixed w-screen h-screen top-0 left-0 flex justify-center items-center bg-black bg-opacity-20 text-black text-xl z-50"
      v-if="props.show"
    >
      <div
        class="fixed top-0 left-0 w-full h-full z-60"
        @click="emit('showEmit', false)"
      ></div>
      <main class="flex flex-col gap-4 p-4 rounded-md bg-white z-70">
        <header class="w-full flex gap-5 items-center justify-between">
          <p><slot name="header"></slot></p>
          <div
            class="i-tabler:x text-2xl cursor-pointer hover:scale-115 transition-all"
            @click="emit('showEmit', false)"
          ></div>
        </header>
        <slot> </slot>
      </main>
    </div>
  </transition>
</template>

<script setup>
const props = defineProps(["show"]);
const emit = defineEmits(["showEmit"]);
</script>

<style>
@keyframes animDialog {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.animDialog-enter-active {
  animation: 100ms animDialog linear;
}

.animDialog-leave-active {
  animation: 100ms animDialog linear reverse;
}
</style>
