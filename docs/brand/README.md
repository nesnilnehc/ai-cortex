# AI Cortex brand

![AI Cortex mark](../../website/favicon.svg)

The [shared SVG mark](../../website/favicon.svg) is the single defining asset for
the website header/footer and browser icon. The repository README uses a plain
text title to keep the introduction compact. An open, angular C surrounds a central node linked
to a horizontal bridge: a compact expression of organized, connected capabilities. The symbol is a visual identity, not a
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

The mark keeps its fixed orange tile and warm-white symbol in both themes.
Interface accents may follow the theme; do not recolor the mark to match them.
The website's [CSS tokens](../../website/styles.css) define interface colors.

## Use

- Reference the SVG directly. Do not redraw it in CSS or keep another editable copy.
- Preserve its square aspect ratio, corner radius, C outline, core node, bridge and colors.
- Allow at least one-quarter of the displayed mark width as surrounding clear space.
- Use 28px for website wordmarks; 16px is the minimum icon size.
- Place it beside the project name where identity needs explanation. Use an empty
  image alt when adjacent text already names the project; otherwise use “AI Cortex mark”.
- Avoid stretching, rotation, shadows, extra outlines or placing text inside the tile.
- Keep the SVG self-contained: no embedded fonts, scripts, external resources or raster images.

## Maintenance

Edit `website/favicon.svg` once, then inspect both website themes.
Website paths use a release query identifier for cache refresh; documentation previews use
repository-relative asset paths. Package the same SVG bytes with the static
site. The established filename is retained for existing browser-icon URLs.

## Adoption and maintenance scope

The Cortex core mark replaces the original stacked bars. The user selected this
vector on 2026-10-23. The personal site mirrors the exact SVG bytes at
`assets/images/ai-cortex.svg`; synchronize it from the canonical asset rather than
editing it independently. The README retains its compact text heading.

This is an asset replacement within the existing header/footer layout, with no
interaction or navigation changes; a separate functional design is not needed.
Check 16px, 28px and 48px rendering against light and dark backgrounds. No trademark
clearance or claim of visual uniqueness is implied.
