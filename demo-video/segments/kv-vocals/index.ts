import { defineSegment } from "videowright";
import { draw, page, ref, SERIF, show, UNDERLINE } from "../../components/kv";

let host: HTMLElement | null = null;

export default defineSegment({
	id: "kv-vocals",
	// 1: "It keeps every human voice..."  2: next segment
	advances: [3.5, 7.4],
	voiceover:
		"A normal vocal remover does not fix this. It keeps every human voice, so the singers stay in your track.",

	mount(el) {
		host = el;
		el.innerHTML = page(
			"keepvoice / 02 &mdash; the usual tool",
			`<h1 data-ref="first" style="${SERIF} font-size: 140px; line-height: 1.05; opacity: 0;">
         A vocal remover<br>does not fix this.</h1>
       <h2 data-ref="second" style="${SERIF} font-size: 120px; line-height: 1.1; font-style: italic; margin-top: 64px; opacity: 0;">
         It keeps every voice, so the
         <span style="position: relative; display: inline-block;">singers<span data-ref="rule" style="${UNDERLINE}"></span></span>
         stay.</h2>`,
		);
	},

	async play(ctx) {
		show(ref(host, "first"));
		await ctx.waitForNext();
		show(ref(host, "second"));
		draw(ref(host, "rule"), 600);
	},

	unmount() {
		host = null;
	},
});
