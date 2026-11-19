// Entry program for the make.fun "Sum up 19 November's world news in one image"
// bounty (news-image-20261119). The image is drawn once and shipped in this
// repository; this program simply copies it to the output directory.
// Node 22+, standard library only, no network access.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
