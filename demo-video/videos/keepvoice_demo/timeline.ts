import "../../styles/editorial-mono/tokens.css";
// Videowright does not load the fonts that the style names, so they are bundled here.
import "@fontsource/instrument-serif/400.css";
import "@fontsource/instrument-serif/400-italic.css";
import "@fontsource/geist/400.css";
import "@fontsource/geist/500.css";
import "@fontsource/jetbrains-mono/400.css";
import type { Timeline } from "videowright";
import defaultAudioTrack from "./audio/tracks/v1/track.js";

const timeline: Timeline = {
	meta: {
		title: "keepvoice demo",
	},
	segments: [
		{ id: "kv-problem" },
		{ id: "kv-vocals", transition: "fade" },
		{ id: "kv-model", transition: "fade" },
		{ id: "kv-result", transition: "fade" },
		{ id: "kv-cta", transition: "fade" },
	],
	default_audio_track: defaultAudioTrack,
};

export default timeline;
