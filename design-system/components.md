# Component Rules

## Use existing primitives first

Before creating new UI, search for existing:

- Button
- Input
- Textarea
- Select
- Checkbox
- Radio
- Switch
- Card
- Badge
- Tabs
- Table
- Dialog
- Dropdown
- Toast
- Sidebar
- Header
- Empty state
- Skeleton/loading state

## Component discipline

- One visual role per component variant.
- Do not create duplicate button styles.
- Do not create one-off cards if a card primitive exists.
- Do not style raw inputs differently from existing inputs.
- Do not introduce new icons unless the icon family already exists.
- Keep disabled, hover, focus, loading, and error states consistent.

## Preferred page recipes

### Dashboard

- Header with title and primary action.
- KPI cards with consistent density.
- Main content grid.
- Secondary panels.
- Empty/error states for each data region.

### Form page

- Clear page title.
- Brief explanatory text.
- Grouped sections.
- Inline validation.
- Sticky or clearly placed submit action for long forms.
- Cancel/back action visually secondary.

### Landing page

- Hero with one primary CTA.
- Supporting proof or explanation.
- Clear section rhythm.
- Scannable cards.
- Trust/support section.
- Final CTA.

### Admin table

- Page title and action area.
- Search/filter row.
- Table with readable density.
- Empty state.
- Pagination.
- Row actions.
- Bulk actions only when needed.
