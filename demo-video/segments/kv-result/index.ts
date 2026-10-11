import { defineSegment } from "videowright";
import { page, ref, SERIF, show } from "../../components/kv";

let host: HTMLElement | null = null;

const CAPTION =
	"font-family: var(--font-body); font-size: 40px; color: var(--color-muted); margin-top: 16px;";

export default defineSegment({
	id: "kv-result",
	// 1: "to below minus eighty-one"  2: "The picture is copied"  3: next segment
	advances: [5.0, 7.4, 10.0],
	voiceover:
		"On a real restaurant video, the song fell from minus thirty-nine decibels, to below minus eighty-one. The picture is copied, bit for bit.",

	mount(el) {
		host = el;
		el.innerHTML = page(
			"keepvoice / 04 &mdash; measured on a real restaurant video",
			`<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px;">
         <div data-ref="before" style="opacity: 0;">
           <div style="${SERIF} font-size: 300px; line-height: 0.95;">&minus;39<span style="font-size: 120px;"> dB</span></div>
           <div style="${CAPTION}">song level, vocal remover</div>
         </div>
         <div data-ref="after" style="opacity: 0;">
           <div style="${SERIF} font-size: 300px; line-height: 0.95; color: var(--color-accent);">&minus;81<span style="font-size: 120px;"> dB</span></div>
           <div style="${CAPTION}">song level, keepvoice: silence</div>
         </div>
       </div>
       <div data-ref="picture" style="
         font-family: var(--font-body); font-size: 52px; font-weight: 500; margin-top: 88px;
         padding-top: 40px; border-top: var(--rule-weight) solid var(--color-border); opacity: 0;
       ">The picture is copied, <em style="${SERIF} font-style: italic; font-size: 64px;">bit for bit.</em></div>`,
		);
	},

	async play(ctx) {
		show(ref(host, "before"));
		await ctx.waitForNext();
		show(ref(host, "after"));
		await ctx.waitForNext();
		show(ref(host, "picture"));
	},

	unmount() {
		host = null;
	},
});
