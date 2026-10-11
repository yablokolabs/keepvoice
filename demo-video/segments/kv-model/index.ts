import { defineSegment } from "videowright";
import { page, ref, SERIF, show } from "../../components/kv";

let host: HTMLElement | null = null;

const STEMS = [
	["speech", "01", "Speech", "your voice"],
	["music", "02", "Music", "instruments and singers"],
	["effects", "03", "Effects", "background noise"],
];

export default defineSegment({
	id: "kv-model",
	// 1: "speech"  2: "music"  3: "effects"  4: "and keeps only the speech"  5: next segment
	advances: [5.5, 6.1, 6.9, 7.7, 9.7],
	voiceover:
		"keepvoice uses a model trained on film sound. It splits the audio into speech, music, and effects, and keeps only the speech.",

	mount(el) {
		host = el;
		const rows = STEMS.map(
			([id, number, name, note]) => `
        <div data-ref="${id}" style="
          display: grid; grid-template-columns: 120px 520px 1fr; align-items: baseline;
          padding: 28px 0; border-top: var(--rule-weight) solid var(--color-border); opacity: 0;
        ">
          <span style="font-family: var(--font-mono); font-size: 28px; color: var(--color-muted);">${number}</span>
          <span data-ref="${id}-name" style="${SERIF} font-size: 104px; line-height: 1;">${name}</span>
          <span style="font-family: var(--font-body); font-size: 44px;">${note}</span>
        </div>`,
		).join("");
		el.innerHTML = page(
			"keepvoice / 03 &mdash; the method",
			`<h1 data-ref="title" style="${SERIF} font-size: 112px; line-height: 1.05; margin-bottom: 56px; opacity: 0;">
         A model trained on <em>film sound.</em></h1>
       ${rows}`,
		);
	},

	async play(ctx) {
		show(ref(host, "title"));
		for (const [id] of STEMS) {
			await ctx.waitForNext();
			show(ref(host, id));
		}
		await ctx.waitForNext();
		const fade = {
			duration: 480,
			fill: "forwards" as const,
			easing: "ease-out",
		};
		ref(host, "music").animate([{ opacity: 1 }, { opacity: 0.22 }], fade);
		ref(host, "effects").animate([{ opacity: 1 }, { opacity: 0.22 }], fade);
		ref(host, "speech-name").animate(
			[{ color: "var(--color-fg)" }, { color: "var(--color-accent)" }],
			fade,
		);
	},

	unmount() {
		host = null;
	},
});
