const filename = "jrlp.js";

module.exports = {
  dev: {
    bundle: true,
    entryPoints: ["src/index.ts"],
    minify: false,
    outfile: `dev/${filename}`,
    platform: "browser",
    tsconfig: "./tsconfig.json",
    color: true,
    sourcemap: true,
    external: ["csharp", "puerts"],
    target: "es2020",
    treeShaking: true,
    logLevel: "error",
    define: {
      "process.env.NODE_ENV": JSON.stringify(
        process.env.NODE_ENV || "development",
      ),
    },
    supported: {
      "async-await": true,
    },
  },
  build: {
    bundle: true,
    entryPoints: ["src/index.ts"],
    minify: true,
    outfile: `dist/${filename}`,
    platform: "browser",
    tsconfig: "./tsconfig.json",
    color: true,
    sourcemap: false,
    external: ["csharp", "puerts"],
    target: "es2020",
    treeShaking: true,
    logLevel: "error",
    define: {
      "process.env.NODE_ENV": JSON.stringify("production"),
    },
    supported: {
      "async-await": true,
    },
  },
};
