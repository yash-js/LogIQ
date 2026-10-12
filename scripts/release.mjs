import { execSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const version = process.argv[2];

function fail(message) {
  console.error(message);
  process.exit(1);
}

function capture(command) {
  return execSync(command, { cwd: root, encoding: "utf8" }).trim();
}

function run(command) {
  execSync(command, { cwd: root, stdio: "inherit" });
}

function compareSemver(a, b) {
  const left = a.split(".").map(Number);
  const right = b.split(".").map(Number);
  for (let i = 0; i < 3; i++) {
    if (left[i] !== right[i]) return left[i] - right[i];
  }
  return 0;
}

function setJsonVersion(path) {
  const text = readFileSync(path, "utf8");
  const next = text.replace(/"version"\s*:\s*"[^"]+"/, `"version": "${version}"`);
  if (next === text) fail(`Could not update the version in ${path}`);
  writeFileSync(path, next);
}

function setCargoPackageVersion() {
  const path = join(root, "src-tauri", "Cargo.toml");
  const text = readFileSync(path, "utf8");
  const next = text.replace(/(\[package\][\s\S]*?^version = ")[^"]+(")/m, `$1${version}$2`);
  if (next === text) fail("Could not update the [package] version in src-tauri/Cargo.toml");
  writeFileSync(path, next);
}

if (!/^\d+\.\d+\.\d+$/.test(version ?? "")) {
  fail("Usage: npm run release <version>   (version must be semver x.y.z, for example 0.1.1)");
}

if (capture("git status --porcelain")) fail("The git working tree is not clean.");
if (capture("git branch --show-current") !== "main") fail("Releases run from the main branch.");

const tauriPath = join(root, "src-tauri", "tauri.conf.json");
const current = JSON.parse(readFileSync(tauriPath, "utf8")).version;
if (!/^\d+\.\d+\.\d+$/.test(current)) fail(`Current version ${current} is not semver x.y.z.`);
if (compareSemver(version, current) <= 0) fail(`${version} is not greater than the current version ${current}.`);

setJsonVersion(tauriPath);
setJsonVersion(join(root, "package.json"));
setCargoPackageVersion();
run("npm install --package-lock-only");

run(`git commit -am "Release v${version}"`);
run(`git tag v${version}`);
run("git push");
run(`git push origin v${version}`);

console.log("https://github.com/yash-js/LogIQ/actions");
