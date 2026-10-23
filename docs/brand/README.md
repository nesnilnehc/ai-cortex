# AI Cortex brand

![AI Cortex mark](../../website/favicon.svg)

The [shared SVG mark](../../website/favicon.svg) is the single defining asset for
the repository README, website header/footer and browser icon. Its three ascending
layers retain the original website motif. The symbol is a visual identity, not a
count of the four asset types. The project name is **AI Cortex**; the website
wordmark uses **AI CORTEX**.

## Palette

| Use | Color |
| --- | --- |
| Mark background / light-mode accent | `#AE4524` |
| Mark foreground | `#FFFAF5` |
| Light page / primary text | `#F6F7F4` / `#202923` |
| Dark page / primary text | `#171C19` / `#E9EEE7` |
| Dark-mode interface accent | `#EC9976` |

The mark keeps its fixed orange tile and warm-white layers in both themes.
Interface accents may follow the theme; do not recolor the mark to match them.
The website's [CSS tokens](../../website/styles.css) define interface colors.

## Use

- Reference the SVG directly. Do not redraw it in CSS or keep another editable copy.
- Preserve its square aspect ratio, corner radius, three layers and colors.
- Allow at least one-quarter of the displayed mark width as surrounding clear space.
- Use 28px for website wordmarks and 64px for the README; 16px is the minimum icon size.
- Place it beside the project name where identity needs explanation. Use an empty
  image alt when adjacent text already names the project; otherwise use “AI Cortex mark”.
- Avoid stretching, rotation, shadows, extra outlines or placing text inside the tile.
- Keep the SVG self-contained: no embedded fonts, scripts, external resources or raster images.

## Maintenance

Edit `website/favicon.svg` once, then inspect the README and both website themes.
Website paths use a release query identifier for cache refresh; the README uses
the repository-relative asset path. Package the same SVG bytes with the static
site. The established filename is retained for existing browser-icon URLs.

This change reuses the existing visual concept and layout without changing
navigation or interaction, so it is a pattern-preserving asset consolidation;
no new functional interaction design or independent mockup is needed.
