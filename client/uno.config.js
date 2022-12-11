import { defineConfig } from "@unocss/vite";

// Unocss presets/transformers
import presetUno from "@unocss/preset-uno";
import presetWebFonts from "@unocss/preset-web-fonts";
import presetRemToPx from "@unocss/preset-rem-to-px";
import presetIcons from "@unocss/preset-icons";

// import transformerCompileClass from "@unocss/transformer-compile-class";
import transformerVariantGroup from "@unocss/transformer-variant-group";

import { presetScrollbar } from "unocss-preset-scrollbar";

export default defineConfig({
  presets: [
    presetUno(),
    presetIcons({
      collections: {
        "line-md": () => import("@iconify-json/line-md").then((i) => i.default),
        "tabler": () => import("@iconify-json/tabler").then((i) => i.default),
      },
    }),
    presetWebFonts({
      provider: "bunny",
      fonts: {
        sans: "Roboto",
        mono: "Roboto Mono",
      },
    }),
    presetRemToPx(),
    presetScrollbar(),
  ],
  transformers: [
    // transformerCompileClass(),
    transformerVariantGroup(),
  ],
});
