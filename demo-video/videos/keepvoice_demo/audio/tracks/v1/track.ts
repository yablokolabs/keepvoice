import type { AudioTrack } from "videowright";

const track: AudioTrack = {
	audio_file: "./audio/tracks/v1/track.mp3",
	length_s: 38.24,
	timing: {
		perSegment: {
			"kv-problem": [1.82, 5.8],
			"kv-vocals": [3.5, 7.44],
			"kv-model": [5.48, 6.1, 6.86, 7.69, 9.71],
			"kv-result": [4.98, 7.44, 10.06],
			"kv-cta": [1.3, 2.38, 5.0],
		},
	},
	audio_plan_path: "../../audio_plan.md",
	plan_snapshot_path: "./plan_snapshot.md",
	created_at: "2026-10-11T19:30:00Z",
};

export default track;
