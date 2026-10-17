"""Validate this atlas layout and export previews; does not generate new artwork."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw


def export(atlas_path: Path, manifest_path: Path, output: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with Image.open(atlas_path) as opened:
        if opened.format != "PNG" or "A" not in opened.getbands():
            raise ValueError("Expected a PNG with an alpha channel")
        atlas = opened.convert("RGBA")
    cell_w, cell_h = manifest["cell_size"]
    columns = manifest["columns"]
    rows = manifest["rows"]
    expected = (columns * cell_w, len(rows) * cell_h)
    if atlas.size != expected:
        raise ValueError(f"Expected atlas size {expected}, got {atlas.size}")
    output.mkdir(parents=True, exist_ok=True)
    all_frames, all_durations = [], []
    populated = 0
    look_frames = []
    for row in rows:
        frames = []
        for column in range(columns):
            left, top = column * cell_w, row["row"] * cell_h
            cell = atlas.crop((left, top, left + cell_w, top + cell_h))
            visible = cell.getchannel("A").getbbox() is not None
            if column >= row["frames"]:
                if visible:
                    raise ValueError(f"Artwork in unused cell ({row['row']}, {column})")
                continue
            if not visible:
                raise ValueError(f"Missing artwork at ({row['row']}, {column})")
            frames.append(cell)
            populated += 1
        if "durations_ms" not in row:
            look_frames.extend(frames)
            continue
        durations = row["durations_ms"]
        if len(durations) != len(frames):
            raise ValueError(f"Timing mismatch for {row['state']}")
        frames[0].save(output / f"{row['state']}.gif", save_all=True,
                       append_images=frames[1:], duration=durations,
                       loop=0, disposal=2, optimize=False)
        for index, (frame, duration) in enumerate(zip(frames, durations)):
            canvas = Image.new("RGB", (cell_w, cell_h + 28), (245, 244, 239))
            canvas.paste(frame, (0, 28), frame.getchannel("A"))
            ImageDraw.Draw(canvas).text((6, 8), f"{row['state']} {index + 1}", fill=(30, 30, 30))
            all_frames.append(canvas)
            all_durations.append(duration)
    all_frames[0].save(output / "all-states.gif", save_all=True,
                       append_images=all_frames[1:], duration=all_durations,
                       loop=0, disposal=2, optimize=False)
    if look_frames:
        look_frames[0].save(output / "look-loop.gif", save_all=True,
                            append_images=look_frames[1:], duration=180,
                            loop=0, disposal=2, optimize=False)
    result = {"ok": True, "required_cells": populated,
              "size": list(atlas.size),
              "sha256": hashlib.sha256(atlas_path.read_bytes()).hexdigest()}
    (output / "validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atlas", type=Path, default=root / "assets/spritesheet.png")
    parser.add_argument("--manifest", type=Path, default=root / "assets/manifest.json")
    parser.add_argument("--output", type=Path, default=root / "build")
    args = parser.parse_args()
    print(json.dumps(export(args.atlas, args.manifest, args.output), indent=2))
