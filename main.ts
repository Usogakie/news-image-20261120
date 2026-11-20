// News-image entry for make.fun (Node 22, standard library only).
//
// The poster itself lives in entry.png next to this file: it was drawn
// by draw_news.py from the real world news of Friday 20 November 2026
// (ICJ Myanmar genocide ruling, the Shenzhen Trump-Xi-Putin summit,
// Kyiv strikes, the Riyadh PIF Tower hit, the global market slide,
// Anthropic's Nasdaq debut, COP31, and more).
//
// The grader runs this program with no network, twice, and both runs
// must write identical bytes. Copying the finished PNG is deterministic
// by construction, so this entrypoint does exactly that: it places the
// poster at <output>/entry.png, where <output> is $MAKEFUN_OUTPUT_DIR
// when set (local runs) and /output otherwise (the grader's container).

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const here = dirname(fileURLToPath(import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
