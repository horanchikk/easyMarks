// Import libs
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { formatDistanceToNowStrict } from "date-fns";
import axios from "axios";

// Import types
import type { Ref } from "vue";

import { useConfig } from "./config";

export const useApi = defineStore("api", () => {
  const config = useConfig();

  async function request(method: string, type: string, data?: any[]) {
    // check core limit
    const result = await axios
      .get(`${config.apiUrl}/rate_limit`)
      .then((res) => {
        if (res.data.resources.core.remaining < 15) {
          return {
            err: {
              type: "limit",
              remaining: res.data.resources.core.remaining,
              reset: formatDistanceToNowStrict(
                new Date(),
                new Date(res.data.resources.core.reset * 1000)
              ),
            },
          };
        } else {
          if (type === "methodRepo") {
            return axios
              .get(`${config.apiUrl}/${method}/${config.repo.full_name}`)
              .then((res) => {
                return res.data;
              })
              .catch((err) => {
                throw err;
              });
          } else if (type === "repoMethod") {
            return axios
              .get(`${config.apiUrl}/repos/${config.repo.full_name}/${method}`)
              .then((res) => {
                return res.data;
              })
              .catch((err) => {
                throw err;
              });
          }
        }
      })
      .catch((err) => {
        throw err;
      });
    return result;
  }

  return {
    request,
  };
});
