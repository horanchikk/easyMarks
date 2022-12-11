<template>
  <input
    :value="props.modelValue"
    @input="updateValue($event.target.value)"
    :class="
      props.dark
        ? `bg-transparent border border-black border-opacity-50 outline-none py-2 px-5 text-xl text-black rounded-md focus:border-opacity-100 placeholder:text-white placeholder:text-opacity-30 transition-all invalid:border-red-400`
        : `bg-transparent border border-white border-opacity-50 outline-none py-2 px-5 text-xl text-white rounded-md focus:border-opacity-100 placeholder:text-white placeholder:text-opacity-30 transition-all invalid:border-red-400`
    "
  />
</template>

<script setup>
const props = defineProps(["modelValue", "dark"]);
const emit = defineEmits(["input", "update:modelValue"]);

function updateValue(value) {
  emit("update:modelValue", value);
}
</script>