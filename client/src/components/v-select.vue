<template>
  <div class="w-full">
    <div :class="show ? 'w-46 p-3 flex items-center justify-between border rounded-t-md select-none cursor-pointer transition-all' : 'w-46 p-3 flex items-center justify-between border rounded-md select-none cursor-pointer transition-all'" @click="show = !show">
      <p>{{ selected }}</p>
      <i :class="show ? 'i-tabler:chevron-up text-xl rotate-180 transition-all' : 'i-tabler:chevron-up text-xl transition-all'"></i>
    </div>
    <Transition name="showSelect" mode="out-in">
      <div class="absolute w-46 overflow-y-scroll flex flex-col bg-black text-black text-opacity-80 rounded-b-md divide-y transition-all" v-show="show">
        <div class="px-3 cursor-pointer select-none py-1 bg-white hover:bg-opacity-80 active:bg-opacity-70 transition-all" @click="emit('item', item[props.objectKey]), show = false, selected = item[props.objectKey]" v-for="item in items" :key="items.length">
          <div>{{ item[props.objectKey] }}</div>
        </div>
      </div>
    </Transition>
  </div>

</template>

<script setup>
import { ref } from 'vue';

const props = defineProps([
    'items', 'objectKey', 'firstItem'
])
const emit = defineEmits([
    'item'
])

const selected = ref(props.firstItem)
const show = ref(false)

</script>

<style>
@keyframes showDown {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}

.showSelect-enter-active {
  animation: showDown 250ms;
}
.showSelect-leave-active {
  animation: showDown 250ms reverse;
}
</style>