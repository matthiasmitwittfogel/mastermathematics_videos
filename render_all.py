#!/usr/bin/env python3
"""Batch render all Manim scenes in the project.

Usage:
    python render_all.py                # Render all scenes at medium quality
    python render_all.py -q l           # Low quality (fast, for testing)
    python render_all.py -q h           # High quality
    python render_all.py --dry-run      # Print what would be rendered without running
    python render_all.py --list         # Only list discovered scenes
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.resolve()

# Try to find manim in PATH (works with `uv run` or activated venv).
_MANIM_PATH = shutil.which("manim")
if _MANIM_PATH:
    MANIM_BIN = Path(_MANIM_PATH)
else:
    MANIM_BIN = None  # validated later in main()

# ---------------------------------------------------------------------------
# Scene discovery
# ---------------------------------------------------------------------------

def discover_scenes() -> list[tuple[Path, str]]:
    """Find all Scene subclasses in shorts/ and videos/."""
    scenes: list[tuple[Path, str]] = []

    # --- shorts --------------------------------------------------------------
    shorts_dir = PROJECT_ROOT / "shorts"
    for py_file in sorted(shorts_dir.glob("*.py")):
        for class_name in _extract_scene_classes(py_file):
            scenes.append((py_file, class_name))

    # --- videos --------------------------------------------------------------
    videos_dir = PROJECT_ROOT / "videos"
    for subdir in sorted(videos_dir.iterdir()):
        if not subdir.is_dir():
            continue
        for py_file in sorted(subdir.glob("*.py")):
            for class_name in _extract_scene_classes(py_file):
                scenes.append((py_file, class_name))

    return scenes


def _extract_scene_classes(filepath: Path) -> list[str]:
    """Extract class names that inherit from Scene or its subclasses."""
    classes: list[str] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            # Match: class Foo(Scene):  or  class Foo(VoiceoverScene):
            # Also catch conditional bases like: class Foo(_Base):
            if stripped.startswith("class ") and "(" in stripped and ")" in stripped:
                base = stripped.split("(", 1)[1].split(")", 1)[0]
                # Accept explicit Scene bases or _Base (common conditional base)
                if "Scene" in base or base == "_Base":
                    name = stripped.split("class ", 1)[1].split("(", 1)[0].strip()
                    classes.append(name)
    return classes


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_scene(
    filepath: Path,
    class_name: str,
    quality: str = "m",
    disable_caching: bool = True,
) -> bool:
    """Render a single Manim scene. Returns True on success."""
    cmd = [
        str(MANIM_BIN),
        f"-q{quality}",
        str(filepath),
        class_name,
    ]
    if disable_caching:
        cmd.append("--disable_caching")

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{PROJECT_ROOT}:{env.get('PYTHONPATH', '')}"

    rel_path = filepath.relative_to(PROJECT_ROOT)
    print(f"\n{'=' * 60}")
    print(f"Rendering: {rel_path}  →  {class_name}")
    print(f"Command:   {' '.join(cmd)}")
    print(f"{'=' * 60}")

    result = subprocess.run(cmd, env=env)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch render all Manim scenes in the project.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality presets:
  l  low      (480p15)   — fastest, for quick testing
  m  medium   (720p30)   — default
  h  high     (1080p60)  — production quality
  k  4k       (2160p60)  — highest quality
        """,
    )
    parser.add_argument(
        "-q", "--quality",
        choices=["l", "m", "h", "k"],
        default="m",
        help="Render quality (default: m)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be rendered without running manim",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Only list discovered scenes and exit",
    )
    parser.add_argument(
        "--no-disable-caching",
        action="store_true",
        help="Allow Manim caching (faster for unchanged scenes)",
    )

    args = parser.parse_args()

    # Validate manim binary
    if MANIM_BIN is None or not MANIM_BIN.exists():
        print("ERROR: Manim not found in PATH.")
        print()
        print("If you installed dependencies with UV, run this script via:")
        print("    uv run python render_all.py")
        print()
        print("Otherwise, ensure manim is installed and available in your PATH.")
        return 1

    # Discover scenes
    scenes = discover_scenes()
    if not scenes:
        print("No scenes found.")
        return 0

    print(f"Discovered {len(scenes)} scene(s):\n")
    for filepath, class_name in scenes:
        rel = filepath.relative_to(PROJECT_ROOT)
        print(f"  {str(rel):60s}  →  {class_name}")

    if args.list:
        return 0

    if args.dry_run:
        print(f"\n(Dry run — {len(scenes)} scene(s) would be rendered)")
        return 0

    # Render
    print(f"\nStarting batch render ({len(scenes)} scene(s), quality={args.quality})\n")
    success = 0
    failed: list[tuple[Path, str]] = []

    for filepath, class_name in scenes:
        if render_scene(
            filepath,
            class_name,
            quality=args.quality,
            disable_caching=not args.no_disable_caching,
        ):
            success += 1
        else:
            failed.append((filepath, class_name))

    # Summary
    print(f"\n{'=' * 60}")
    print(f"BATCH RENDER COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Success : {success}/{len(scenes)}")
    print(f"  Failed  : {len(failed)}/{len(scenes)}")

    if failed:
        print(f"\nFailed scenes:")
        for filepath, class_name in failed:
            rel = filepath.relative_to(PROJECT_ROOT)
            print(f"  ✗ {rel} → {class_name}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
