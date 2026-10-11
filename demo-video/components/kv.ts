// Shared layout and motion for the keepvoice segments (editorial-mono style).

const EASE = "cubic-bezier(0.16, 1, 0.3, 1)";

/** Full-frame page: mono label and hairline rule at the top, body below. */
export function page(label: string, body: string): string {
	return `
    <div style="
      position: relative; height: 100%; box-sizing: border-box; overflow: hidden;
      background: var(--color-bg); color: var(--color-fg);
      padding: var(--safe-y) var(--safe-x);
      display: flex; flex-direction: column;
    ">
      <div style="
        font-family: var(--font-mono); font-size: 22px; letter-spacing: 0.16em;
        text-transform: uppercase; color: var(--color-muted);
        padding-bottom: 24px; border-bottom: var(--rule-weight) solid var(--color-fg);
      ">${label}</div>
      <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
        ${body}
      </div>
    </div>`;
}

export function ref(host: HTMLElement | null, name: string): HTMLElement {
	return host?.querySelector(`[data-ref="${name}"]`) as HTMLElement;
}

/** Fade in while settling upward by 16px. */
export function show(el: HTMLElement, delay = 0): void {
	el.animate(
		[
			{ opacity: 0, transform: "translateY(16px)" },
			{ opacity: 1, transform: "translateY(0)" },
		],
		{ duration: 480, delay, fill: "forwards", easing: EASE },
	);
}

/** Draw a red rule from left to right under its parent. */
export function draw(el: HTMLElement, delay = 0): void {
	el.animate([{ width: "0%" }, { width: "100%" }], {
		duration: 480,
		delay,
		fill: "forwards",
		easing: EASE,
	});
}

export const SERIF =
	"font-family: var(--font-display); font-weight: 400; margin: 0;";
export const UNDERLINE =
	"position: absolute; left: 0; bottom: -6px; height: 8px; width: 0; background: var(--color-accent);";
