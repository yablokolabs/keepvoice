import type { Voiceover } from "videowright";

const voiceover: Voiceover = {
	audio_file: "./audio.mp3",
	provider: "elevenlabs",
	provider_timing_file: "./timing.json",
	eleven_labs_voice_id: "Xb7hH8MSUJpSbSDYk0k2", // Alice
	timing: {
		perSegment: {
			"kv-problem": [1.82, 5.8],
			"kv-vocals": [3.5, 7.44],
			"kv-model": [5.48, 6.1, 6.86, 7.69, 9.71],
			"kv-result": [4.98, 7.44, 10.06],
			"kv-cta": [1.3, 2.38, 5.0],
		},
	},
	notes: "British female voice, clear and steady",
};

export default voiceover;
