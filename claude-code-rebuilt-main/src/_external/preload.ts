import { plugin } from "bun";

const version = process.env.CLI_VERSION || "99.0.0-external";

(globalThis as any).MACRO = {
  VERSION: version,
  BUILD_TIME: new Date().toISOString(),
  PACKAGE_URL: "https://www.npmjs.com/package/@anthropic-ai/claude-code",
  NATIVE_PACKAGE_URL: "",
  VERSION_CHANGELOG: "",
  FEEDBACK_CHANNEL: "",
  ISSUES_EXPLAINER: "https://github.com/anthropics/claude-code/issues",
};

plugin({
  name: "bun-bundle-shim",
  setup(build) {
    build.module("bun:bundle", () => {
      return {
        exports: {
          feature: (_name: string): boolean => false,
        },
        loader: "object",
      };
    });
  },
});
