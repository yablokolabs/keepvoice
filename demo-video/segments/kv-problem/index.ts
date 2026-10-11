import { defineSegment } from "videowright";
import { page, ref, SERIF, show } from "../../components/kv";

let host: HTMLElement | null = null;

export default defineSegment({
	id: "kv-problem",
	// 1: "But a song is playing..."  2: next segment
	advances: [1.8, 5.8],
	voiceover:
		"You recorded a video. But a song is playing in the background, and that song is copyrighted.",

	mount(el) {
		host = el;
		el.innerHTML = page(
			"keepvoice / 01 &mdash; the problem",
			`<h1 data-ref="first" style="${SERIF} font-size: 176px; line-height: 1; white-space: nowrap; opacity: 0;">
         You recorded a video.</h1>
       <h2 data-ref="second" style="${SERIF} font-size: 120px; line-height: 1.1; margin-top: 56px; opacity: 0;">
         But the song in the background<br>is <em style="color: var(--color-accent);">copyrighted.</em></h2>`,
		);
	},

	async play(ctx) {
		show(ref(host, "first"));
		await ctx.waitForNext();
		show(ref(host, "second"));
	},

	unmount() {
		host = null;
	},
});
