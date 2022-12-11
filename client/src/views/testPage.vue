<template>
  <!-- For dialogs -->
  <vDialog :show="showTest" @show-emit="changeShow">
    <template v-slot:header>
      <p class="text-xl font-bold">This is header</p>
    </template>
    <div class="p-3 text-center">Here is your info</div>
    <vInput dark="true" class="text-black" placeholder="Here is input" />
    <div class="flex gap-3">
      <vButton type="success">button</vButton>
      <vButton type="warning">button</vButton>
      <vButton type="error">button</vButton>
    </div>
  </vDialog>

  <vDialog :show="showTest2" @show-emit="changeShow">
    <template v-slot:header>
      <p class="text-xl font-bold text-orange-500">Random photos</p>
    </template>
    <div class="flex justify-center p-2">
      <div
        v-if="image !== undefined"
        class="flex flex-col gap-3 justify-center items-center"
      >
        <img
          :src="image"
          alt="random image"
          loading="lazy"
          class="rounded-lg shadow transition-all  shadow-black shadow-opacity-50 hover:shadow-md"
        />
        <vButton type="success" @click="generate">Generate new</vButton>
      </div>
      <div v-else class="p-5 text-2xl i-line-md:loading-loop"></div>
    </div>
  </vDialog>

  <!-- Main container -->
  <div class="flex overflow-y-scroll flex-col w-full h-full">
    <div class="py-5 w-full font-mono text-3xl font-bold text-center">
      Our design
    </div>
    <div class="flex flex-col flex-auto gap-5 justify-center items-center">
      <section>
        <p class="my-3 w-full text-xl text-center">Buttons</p>
        <div class="flex flex-col gap-3 p-5 rounded-md border">
          <vButton class="border-animated">
            <div class="text-xl i-line-md:loading-loop"></div>
            <p>Loading</p>
          </vButton>
          <vButton type="success">Success</vButton>
          <vButton type="warning">Warning</vButton>
          <vButton type="error">Error</vButton>
        </div>
      </section>
      <section>
        <p class="my-3 w-full text-xl text-center">Inputs</p>
        <div class="flex flex-col gap-3 p-5 rounded-md border">
          <vInput name="lol" placeholder="default" />
          <form>
            <vInput name="lol" placeholder="required" required />
          </form>
        </div>
      </section>
      <section>
        <p class="my-3 w-full text-xl text-center">Icons</p>
        <div class="p-5 rounded-md border">
          <!-- <iframe
            src="https://tabler-icons.io/"
            frameborder="0"
            width="500"
            height="300"
          ></iframe> -->
        </div>
      </section>
      <section>
        <p class="my-3 w-full text-xl text-center">Dialog</p>
        <div class="flex flex-col gap-3 p-5 rounded-md border">
          <vButton type="warning" @click="showTest = true">Show dialog</vButton>
          <vButton
            type="warning"
            @click="
              showTest2 = true;
              generate();
            "
            >Show random image</vButton
          >
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import vButton from "../components/v-button.vue";
import vInput from "../components/v-input.vue";
import vDialog from "../components/v-dialog.vue";
import axios from "axios";
import { ref } from "vue";

const showTest = ref(false);
const showTest2 = ref(false);
const image = ref(undefined);

function changeShow(state) {
  showTest.value = state;
  showTest2.value = state;
}

function generate() {
  image.value = undefined;
  axios.get("https://picsum.photos/600/600?random=1").then((res) => {
    image.value = res.request.responseURL;
  });
}
</script>
