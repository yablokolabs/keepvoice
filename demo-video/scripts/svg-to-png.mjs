// Convert each SVG in docs/diagrams to a PNG at 2x, with the web fonts loaded.
// Run from demo-video/: node scripts/svg-to-png.mjs
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "@playwright/test";

const dir = join(
	dirname(fileURLToPath(import.meta.url)),
	"../../docs/diagrams",
);
const browser = await chromium.launch();
for (const file of readdirSync(dir).filter((name) => name.endsWith(".svg"))) {
	const svg = readFileSync(join(dir, file), "utf8");
	const [, width, height] = svg.match(/viewBox="0 0 (\d+) (\d+)"/).map(Number);
	const page = await browser.newPage({
		viewport: { width, height },
		deviceScaleFactor: 2,
	});
	await page.setContent(
		`<style>body{margin:0}svg{display:block;width:${width}px}</style>${svg}`,
	);
	await page.evaluate(() => document.fonts.ready);
	await page.waitForLoadState("networkidle");
	await page.screenshot({ path: join(dir, file.replace(/\.svg$/, ".png")) });
	await page.close();
}
await browser.close();
