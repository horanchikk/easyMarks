<template>
  <button
    v-if="props.type === 'success'"
    class="border-green-6 px-8 py-2 rounded-md shadow-md shadow-black shadow-opacity-20 flex justify-center items-center gap-2 border outline-none active:border-green-7 hover:(shadow-opacity-10, border-green-5) transition-all"
  >
    <slot />
  </button>
  <button
      v-else-if="props.type === 'loading'"
      class="border border-opacity-10 px-8 py-2 rounded-md shadow-md shadow-black shadow-opacity-20 flex justify-center items-center gap-2 border outline-none transition-all"
  >
    <span class="i-line-md:loading-loop"></span>
    Вход на сервер...
  </button>
  <button
    v-else-if="props.type === 'warning'"
    class="border-yellow-6 px-8 py-2 rounded-md shadow-md shadow-black shadow-opacity-40 flex justify-center items-center gap-2 border outline-none active:border-yellow-7 hover:(shadow-opacity-10, border-yellow-5) transition-all"
  >
    <slot />
  </button>
  <button
    v-else-if="props.type === 'error'"
    class="border-red-6 px-8 py-2 rounded-md shadow-md shadow-black shadow-opacity-40 flex justify-center items-center gap-2 border outline-none active:border-red-7 hover:(shadow-opacity-10, border-red-5) transition-all"
  >
    <slot />
  </button>
  <button
    v-else
    class="px-8 py-2 rounded-md shadow-md shadow-black shadow-opacity-10 flex items-center justify-center gap-2 outline-none transition-all"
  >
    <slot />
  </button>
</template>

<script setup>
const props = defineProps(["type"]);

// icons - https://cyberalien.github.io/line-md/
</script>
