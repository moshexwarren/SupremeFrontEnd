# RTL Rules

Use this for Hebrew, Arabic, or mixed-direction products.

## Required checks

- Page direction is correct.
- Text alignment is intentional.
- Icons that imply direction are mirrored when needed.
- Breadcrumbs and step indicators make sense in RTL.
- Form labels and validation messages align correctly.
- Tables keep numeric values readable.
- Mixed English/Hebrew text does not scramble punctuation.
- Sidebar and navigation placement are intentional.
- Mobile drawers open from the expected side.

## Avoid

- Hardcoded `left`/`right` when logical CSS properties would work.
- Icons like arrows, chevrons, back/forward symbols without RTL review.
- Assuming English line-height and font metrics fit Hebrew.

Prefer:

- `margin-inline-start` / `margin-inline-end`
- `padding-inline-start` / `padding-inline-end`
- `inset-inline-start` / `inset-inline-end`
- `text-align: start`
