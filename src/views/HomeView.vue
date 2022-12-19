<template>
  <main
    class="w-full h-full flex flex-col py-5 items-center justify-center gap-6 showAnim"
  >
    <p class="text-xl text-white">{{ repo.name }} stats</p>
    <section
      class="w-2/3 h-2/4 flex flex-col border rounded-md cursor-default text-white bg-black bg-opacity-20"
    >
      <p class="w-full text-center my-2">Last 30 published commits</p>
      <!--  We are not using table elem bcs we need in overflow y scroll :(-->
      <main class="flex-auto flex flex-col px-2">
        <section class="flex justify-between text-center">
          <div class="w-1/4 border">Message</div>
          <div class="w-1/4 border">Committer</div>
          <div class="w-1/4 border">Date</div>
          <div class="w-1/4 border">Url</div>
        </section>
        <section class="flex-auto overflow-y-scroll scrollbar h-1">
          <div class="w-full h-full">
            <div
              v-for="commit in commits"
              :key="commit.sha"
              class="flex justify-between bg-white bg-opacity-0 text-stone-400 hover:text-white hover:bg-opacity-10 transition-all"
            >
              <div class="truncate w-1/4 p-2 border opacity-90">
                {{ commit.commit.message }}
              </div>
              <div
                class="w-1/4 border flex items-center justify-center opacity-90"
              >
                <a
                  :href="`https://github.com/${commit.committer.login}`"
                  target="_blank"
                  >{{ commit.committer.login }}</a
                >
              </div>
              <div
                class="w-1/4 border flex items-center justify-center opacity-90"
              >
                {{
                  format(
                    parseISO(commit.commit.committer.date),
                    "dd.MM.yyyy hh:mm"
                  )
                }}
              </div>
              <div
                class="w-1/4 border flex items-center justify-center opacity-90"
              >
                <a :href="commit.html_url" target="_blank">Click</a>
              </div>
            </div>
          </div>
        </section>
      </main>
    </section>
    <section
      class="w-2/3 h-2/4 flex flex-col gap-2 border rounded-md text-white bg-black bg-opacity-20"
    >
      <p class="w-full text-center my-2 cursor-default">Tasks</p>
      <div
        class="flex-auto flex flex-col items-center shrink scrollbar overflow-y-scroll h-1 px-2"
      >
        <div
          v-if="issues.length < 0"
          class="w-full h-full flex items-center justify-center text-white"
        >
          There are no tasks.
        </div>
        <div
          v-else
          v-for="issue in issues"
          v-show="issue.state === 'open'"
          :key="issue.number"
          class="flex gap-5"
        >
          <a :href="issue.html_url" target="_blank">{{ issue.title }}</a>
          <p
            v-for="label in issue.labels"
            :key="label.id"
            class="flex items-center justify-center rounded-full text-sm border px-2 cursor-pointer opacity-70 hover:opacity-100 transition-all"
            :style="{
              color: `#${label.color}`,
              borderColor: `#${label.color}`,
            }"
          >
            {{ label.name }}
          </p>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
// Import libs
import { ref } from "vue";
import { useApi } from "@/stores/api";
import { format, parseISO } from "date-fns";

// Import types
import type { Ref } from "vue";

const api = useApi();

const repo: Ref<object> = ref(await api.request("repos", "methodRepo"));
const commits: Ref<object> = ref(await api.request("commits", "repoMethod"));
const issues: Ref<object> = ref(await api.request("issues", "repoMethod"));
</script>
