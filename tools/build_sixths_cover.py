"""Source-free, user-requested 1/6 geometric-series cover.

The first 23 source-derived covers are deliberately left untouched.
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--studio', type=Path, required=True)
    args = parser.parse_args()
    repo, studio = args.repo.resolve(), args.studio.resolve()
    sys.path.insert(0, str(studio / 'tools'))
    from cover_layout import render
    from runtime_paths import font_path

    spec = importlib.util.spec_from_file_location('existing_cover_helpers', repo / 'tools/build_covers.py')
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)
    work = repo / 'work/sixths_cover'
    work.mkdir(parents=True, exist_ok=True)
    helpers.WORK = work
    helpers.REGULAR = regular = font_path('arial.ttf')
    helpers.BOLD = bold = font_path('arialbd.ttf')

    navy, blue, green = '#0B1020', '#528BFF', '#46D68C'
    diagram = Image.new('RGB', (1720, 1640), navy)
    draw = ImageDraw.Draw(diagram)
    helpers.formula(diagram, r'\frac{1}{6}+\left(\frac{1}{6}\right)^2+\cdots=?', (860, 170), height=210)
    helpers.txt(draw, (860, 380), 'A unit square', 72, blue)

    # Each chosen cell has 1/6 of its parent's area. The next recursion uses
    # another (disjoint) cell, so the green regions represent a sum, not overlap.
    bounds = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))
    regions, grids = [], []
    for level in range(4):
        x, y, w, h = bounds
        cols, rows = (3, 2) if level % 2 == 0 else (2, 3)
        cell_w, cell_h = w / cols, h / rows
        selected = (x, y, cell_w, cell_h)
        assert cell_w * cell_h == Fraction(1, 6 ** (level + 1))
        regions.append(selected)
        grids.append((bounds, cols, rows))
        bounds = (x + (cols - 1) * cell_w, y + (rows - 1) * cell_h, cell_w, cell_h)

    def point(x, y):
        return (330 + float(x) * 1060, 460 + float(y) * 1060)

    for x, y, w, h in regions:
        draw.rectangle((*point(x, y), *point(x + w, y + h)), fill=green)
    for (x, y, w, h), cols, rows in grids:
        for col in range(cols + 1):
            xx = x + w * Fraction(col, cols)
            draw.line([point(xx, y), point(xx, y + h)], fill=blue, width=8)
        for row in range(rows + 1):
            yy = y + h * Fraction(row, rows)
            draw.line([point(x, yy), point(x + w, yy)], fill=blue, width=8)
    # Keep the first term legible without tiny labels in the recursive cells.
    label = Image.new('RGB', (220, 180), green)
    from PIL import ImageFont
    ld = ImageDraw.Draw(label)
    font = ImageFont.truetype(str(bold), 85)
    ld.text((110, 90), '1/6', font=font, fill=navy, anchor='mm')
    cx, cy = point(Fraction(1, 6), Fraction(1, 4))
    diagram.paste(label, (round(cx - 110), round(cy - 90)))

    cfg = dict(headline=['An endless', 'sum'], subtitle='Start at one sixth', prompt='WHERE DOES IT END?')
    cover = render(cfg, diagram, regular, bold, scale=2)
    output = repo / 'covers/geometric_series_from_one_over_6.jpg'
    output.parent.mkdir(exist_ok=True)
    cover.save(output, quality=96, subsampling=0, optimize=True)
    cover.resize((360, 640), Image.Resampling.LANCZOS).save(work / 'mobile.jpg', quality=96, subsampling=0)
    with Image.open(output) as check:
        check.load()
        assert check.size == (2160, 3840) and check.format == 'JPEG'
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = dict(
        status='pending_visual_and_math_review', output=output.relative_to(repo).as_posix(),
        output_sha256=sha(output), renderer_sha256=sha(Path(__file__)),
        helper_sha256=sha(repo / 'tools/build_covers.py'), layout_sha256=sha(studio / 'tools/cover_layout.py'),
        regular_font_sha256=sha(regular), bold_font_sha256=sha(bold),
        provenance='No original video source. New diagram requested by user, based on specified series.',
        layout='studio-cover-v1', size=[2160, 3840], colors=dict(fill=green, lines=blue),
        mathematical_model=dict(first_term='1/6', ratio='1/6', convergence='abs(ratio)<1', sum='1/5',
                                green_areas=[str(r[2] * r[3]) for r in regions],
                                construction='Alternating 3x2 and 2x3 grids; shade upper-left cell, recurse in lower-right cell. Regions are disjoint.'),
        answer_shown=False,
    )
    (work / 'build.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(dict(output=str(output), size=[2160, 3840], sha256=sha(output))))


if __name__ == '__main__':
    main()
