#!/usr/bin/env python3
"""
Create a boomerang-style infinite loop video from an input video.
- Slows down the beginning and end of the video
- Duplicates the video (2x length) with the second half reversed
- Creates seamless transitions at the turnaround and loop points
"""

import json
import subprocess
import sys
from pathlib import Path

# Configurable parameters
INPUT_VIDEO = "video.mp4"
OUTPUT_VIDEO = "video_boomerang.mp4"
SLOW_PCT = 0.15  # 15% of video slowed at each end
SLOW_FACTOR = 1.3  # 1.3x slower at beginning and end
SPEED_UP = 1.7  # Speed up entire output by this factor
CROP_TOP = 80  # Pixels to crop from top (removes watermark); aspect ratio preserved
CRF = 23  # Encoding quality (lower = better quality, larger file)


def get_video_info(video_path: str) -> tuple[float, int, int]:
    """Get video duration (seconds), width, and height using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    duration = float(data["format"]["duration"])
    video_stream = next(s for s in data["streams"] if s["codec_type"] == "video")
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return duration, width, height




def run_ffmpeg(args: list[str], description: str) -> None:
    """Run ffmpeg and print progress."""
    print(f"  {description}...")
    result = subprocess.run(
        ["ffmpeg", "-y"] + args,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise SystemExit(f"FFmpeg failed: {description}")


def main() -> None:
    input_path = Path(INPUT_VIDEO)
    if not input_path.exists():
        raise SystemExit(f"Input video not found: {input_path}")

    print("Creating boomerang video...")
    duration, width, height = get_video_info(str(input_path))
    slow_dur = duration * SLOW_PCT
    mid_start = slow_dur
    mid_end = duration - slow_dur

    # Crop dimensions: remove top, keep 16:9 aspect ratio (even dimensions for codec)
    crop_h = ((height - CROP_TOP) // 2) * 2
    crop_w = (int(crop_h * 16 / 9) // 2) * 2
    crop_x = (width - crop_w) // 2
    crop_y = CROP_TOP

    # Temporary files
    processed_path = input_path.parent / "processed_boomerang_temp.mp4"
    reversed_path = input_path.parent / "reversed_boomerang_temp.mp4"
    concat_path = input_path.parent / "concat_boomerang_temp.mp4"
    concat_list_path = input_path.parent / "concat_list_temp.txt"

    try:
        # Step 1: Crop (remove watermark) + apply slow zones to create processed.mp4
        # Three segments: slow_start | normal_middle | slow_end
        crop_filter = f"crop={crop_w}:{crop_h}:{crop_x}:{crop_y}"
        filter_parts = [
            f"[0:v]{crop_filter}[c];[c]split=3[c0][c1][c2]",
            f"[c0]trim=start=0:end={slow_dur},setpts={SLOW_FACTOR}*(PTS-STARTPTS)[v0]",
            f"[c1]trim=start={mid_start}:end={mid_end},setpts=PTS-STARTPTS[v1]",
            f"[c2]trim=start={mid_end}:end={duration},setpts={SLOW_FACTOR}*(PTS-STARTPTS)[v2]",
            "[v0][v1][v2]concat=n=3:v=1:a=0[outv]",
        ]
        filter_complex = ";".join(filter_parts)

        run_ffmpeg(
            [
                "-i", str(input_path),
                "-filter_complex", filter_complex,
                "-map", "[outv]",
                "-an",  # Strip audio for simplicity; add -map 0:a? to preserve if needed
                "-c:v", "libx264",
                "-crf", str(CRF),
                "-preset", "medium",
                str(processed_path),
            ],
            "Step 1: Applying slow zones",
        )

        # Step 2: Reverse processed.mp4 → reversed.mp4
        run_ffmpeg(
            [
                "-i", str(processed_path),
                "-vf", "reverse",
                "-an",
                "-c:v", "libx264",
                "-crf", str(CRF),
                "-preset", "medium",
                str(reversed_path),
            ],
            "Step 2: Reversing video",
        )

        # Step 3: Concatenate processed + reversed → temp file
        concat_list_path.write_text(
            f"file '{processed_path.absolute()}'\n"
            f"file '{reversed_path.absolute()}'\n"
        )

        run_ffmpeg(
            [
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_list_path),
                "-c", "copy",
                str(concat_path),
            ],
            "Step 3: Concatenating forward + reversed",
        )

        # Step 4: Speed up entire video by SPEED_UP factor
        output_path = input_path.parent / OUTPUT_VIDEO
        run_ffmpeg(
            [
                "-i", str(concat_path),
                "-vf", f"setpts=PTS/{SPEED_UP}",
                "-an",
                "-c:v", "libx264",
                "-crf", str(CRF),
                "-preset", "medium",
                str(output_path),
            ],
            "Step 4: Speeding up video",
        )

        print(f"\nDone! Output saved to: {output_path}")
    finally:
        # Clean up temp files
        for p in [processed_path, reversed_path, concat_path, concat_list_path]:
            if p.exists():
                p.unlink()
                print(f"  Removed temp: {p.name}")


if __name__ == "__main__":
    main()
