import { defineSegment } from "videowright";
import { page, ref, SERIF, show } from "../../components/kv";

let host: HTMLElement | null = null;

export default defineSegment({
	id: "kv-cta",
	// 1: "Open source"  2: "keepvoice"  3: end of video
	advances: [1.3, 2.4, 5.0],
	voiceover: "One command. Open source. keepvoice.",

	mount(el) {
		host = el;
		el.innerHTML = page(
			"keepvoice / 05 &mdash; open source",
			`<h1 data-ref="name" style="${SERIF} font-size: 260px; line-height: 1; font-style: italic; opacity: 0;">keepvoice</h1>
       <div data-ref="command" style="
         font-family: var(--font-mono); font-size: 64px; margin-top: 72px; opacity: 0;
       ">$ keepvoice video.mp4</div>
       <div data-ref="source" style="
         font-family: var(--font-body); font-size: 44px; margin-top: 40px; opacity: 0;
       ">MIT licence &middot; <span style="color: var(--color-accent);">github.com/yablokolabs/keepvoice</span></div>`,
		);
	},

	async play(ctx) {
		show(ref(host, "command"));
		await ctx.waitForNext();
		show(ref(host, "source"));
		await ctx.waitForNext();
		show(ref(host, "name"));
	},

	unmount() {
		host = null;
	},
});
