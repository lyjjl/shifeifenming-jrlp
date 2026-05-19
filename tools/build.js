const { buildSync } = require("esbuild");
const path = require("node:path");
const fs = require("node:fs");
const configAll = require("./build-config");

(async () => {
  try {
    const buildEnv = process.env.NODE_ENV;
    const config = buildEnv === "production" ? configAll.build : configAll.dev;

    const timerStart = Date.now();
    fs.rmSync(path.dirname(config.outfile), { recursive: true, force: true });

    buildSync(config);
    const bodyText = fs.readFileSync(config.outfile);
    const headerText = fs.readFileSync("./header.txt").toString();
    fs.writeFileSync(config.outfile, `${headerText}\n${bodyText}`);
    const timerEnd = Date.now();
    console.log(`🔨 Built in ${timerEnd - timerStart}ms.`);
    process.exit(0);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
