// The Daily Globe — Friday 27 November 2026 (safety edition).
// Entry point for make.fun news-image-20261127. Node 22, standard library
// only. Copies the pre-drawn entry.png (built locally by draw27.py)
// to the grader's output directory. Deterministic: same bytes every run.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error(`entry.png missing next to main.ts (${source})`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
console.log(`wrote ${target} (${statSync(target).size} bytes)`);
