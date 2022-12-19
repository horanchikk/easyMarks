// Import libs
import { defineStore } from "pinia";

export const useConfig = defineStore("config", () => {
  // Interfaces
  interface Repo {
    full_name: string; // {owner}/{repo}
    token?: string; // if repository is private
  }

  //   Values
  const repo: Repo = {
    full_name: "horanchikk/markSystem",
  };
  const apiUrl = <string>"https://api.github.com"; // link of git hosting

  return { repo, apiUrl };
});
