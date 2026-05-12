# MasterMathematics

Math animation scenes for the [MasterMathematics](https://www.youtube.com/channel/UCJ0KfcrJnTDGwFDXcPe6MZQ) YouTube channel.

---

## Quick Start

### 1. Install UV

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> UV is a fast Python package manager. You only need to install it once.

### 2. Clone & Setup

```bash
git clone <your-repo-url>
cd mastermathematics
uv sync
```

`uv sync` reads `pyproject.toml` + `uv.lock` and installs **exactly** the same dependency versions (including ManimCE 0.20.1).

### 3. Render a Scene

```bash
# Render a single scene
uv run manim -pqm shorts/20230905_apple_logo.py AppleLogo

# Render all scenes
uv run python render_all.py
```

Quality presets:
- `-ql` = low (480p15) — fastest, for testing
- `-qm` = medium (720p30) — default
- `-qh` = high (1080p60)
- `-qk` = 4K (2160p60)

> **Tip:** `render_all.py` never auto-plays videos after rendering. Add `-p` if you want preview.

---

## Optional: Voiceover

Some scenes use `manim-voiceover` with Azure TTS. Voiceover is **disabled by default** — all scenes run fine without it.

To enable voiceover:

1. Install the voiceover extra:
   ```bash
   uv sync --extra voiceover
   ```

2. Fill in your Azure credentials in `.env`:
   ```
   AZURE_SUBSCRIPTION_KEY=your-key-here
   AZURE_SERVICE_REGION=your-region-here
   ```

3. Re-run the scene.

---

## Introduction

This repo contains the ManimCE source code for math animations published on the MasterMathematics channel.

| File | YouTube |
|:-----|:--------|
| [20230905_apple_logo.py](shorts%2F20230905_apple_logo.py) | [Short](https://www.youtube.com/shorts/_JcG53_koAc) |
| [20230907_sum_from_1_to_n.py](shorts%2F20230907_sum_from_1_to_n.py) | [Short](https://www.youtube.com/shorts/DcpvZphAmtE) |
| [20230907_sum_from_1_over_2_to_1_over_64.py](shorts%2F20230907_sum_from_1_over_2_to_1_over_64.py) | [Short](https://www.youtube.com/shorts/pZ9D7cVGfXg) |
| [20230909_a_plus_b_square.py](shorts%2F20230909_a_plus_b_square.py) | [Short](https://www.youtube.com/shorts/6YCmP_YI2y0) |
| [20230910_difference_of_squares.py](shorts%2F20230910_difference_of_squares.py) | [Short](https://www.youtube.com/shorts/7xLBwvQVkks) |
| [20230913_find_shaded_area.py](shorts%2F20230913_find_shaded_area.py) | [Short](https://www.youtube.com/shorts/hM80vKYMGyY) |
| [20230916_bubble_sort_algorithm.py](shorts%2F20230916_bubble_sort_algorithm.py) | [Short](https://www.youtube.com/shorts/DdLTrfpylfw) |
| [20230919_circle_area.py](shorts%2F20230919_circle_area.py) | [Short](https://www.youtube.com/shorts/llM5NW0j-k0) |
| [20230925_sum_from_1_to_2n_1.py](shorts%2F20230925_sum_from_1_to_2n_1.py) | [Short](https://www.youtube.com/shorts/-1SY4wm9QNQ) |
| [20230927_sum_1_to_n_to_1.py](shorts%2F20230927_sum_1_to_n_to_1.py) | [Short](https://www.youtube.com/shorts/XTVIPywgwDY) |
| [20231001_febonacci_square_sum.py](shorts%2F20231001_febonacci_square_sum.py) | [Short](https://www.youtube.com/shorts/g17zLAkW4iA) |
| [20231003_series_sum_from_one_over8.py](shorts%2F20231003_series_sum_from_one_over8.py) | [Short](https://www.youtube.com/shorts/pRvgyhpcdII) |
| [20231008_a_plus_b__plus_c_square.py](shorts%2F20231008_a_plus_b__plus_c_square.py) | [Short](https://www.youtube.com/shorts/PXQgORj1AQo) |
| [20231008_insertion_sort_animation.py](shorts%2F20231008_insertion_sort_animation.py) | [Short](https://www.youtube.com/shorts/4cmuJJISfPY) |
| [20231010_selection_sort.py](shorts%2F20231010_selection_sort.py) | [Short](https://www.youtube.com/shorts/yPilRFA2ZMM) |
| [20231021_infinite_series_from_1_over_2.py](shorts%2F20231021_infinite_series_from_1_over_2.py) | [Short](https://www.youtube.com/shorts/eFJHXx-xyZ0) |
| [20231025_1_over_3_series.py](shorts%2F20231025_1_over_3_series.py) | [Short](https://www.youtube.com/shorts/OhZ4BSQNqUU) |
| [20231031_bytedance_logo.py](shorts%2F20231031_bytedance_logo.py) | [Short](https://www.youtube.com/shorts/JuBcZKQRv_w) |
| [20240416_mirror_equation.py](shorts%2F20240416_mirror_equation.py) | [Short](https://www.youtube.com/shorts/E_v4qAUGNUI) |
| [20231025_express_love_with_formulas](videos%2F20231025_express_love_with_formulas) | [Video](https://www.youtube.com/watch?v=v_xEl70TM8c) |
| [20231104_cube_sum](videos%2F20231104_cube_sum) | [Video](https://www.youtube.com/watch?v=r5itGj29gh8&t=24s) |
| [20231107_china_flag](videos%2F20231107_china_flag) | [Video](https://www.youtube.com/watch?v=G3FpbKVKlCg) |
| [20240416_bubble_sort](videos%2F20240416_bubble_sort) | [Video](https://www.youtube.com/watch?v=YUuUKpOJqnE) |
