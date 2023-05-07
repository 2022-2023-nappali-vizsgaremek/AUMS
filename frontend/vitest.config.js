import { mergeConfig } from "vite"
import viteConfig from "./vite.config"
import { fileURLToPath } from "node:url"
import { configDefaults, defineConfig } from "vitest/config"

export default mergeConfig(
    viteConfig,
    defineConfig(
    {
        test:
        {
            environment: "jsdom",
            exclude: [...configDefaults.exclude, "e2e/*"],
            root: fileURLToPath(new URL("./", import.meta.url))
        }
    })
)