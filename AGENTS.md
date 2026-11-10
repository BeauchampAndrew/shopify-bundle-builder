# Agent guide: Build-Your-Own Bundle for Shopify

Instructions for AI coding agents (Claude Code, Cursor, Codex, etc.) installing, rebranding or extending this section. Humans should start with [README.md](README.md).

## What this is

A single Shopify theme section, `sections/bundle-builder.liquid`, that renders a "build your box" page:

1. **Box sizes** (blocks of type `size`): each has an item count, a percent discount, a discount code and an optional badge.
2. **Product categories** (blocks of type `category`): a collection or a hand-picked product list, rendered as cards with + Add / − qty + steppers.
3. **Prebuilt bundles** (blocks of type `preset`): buttons that fill the box with a set list of products.
4. **The builder panel:** size picker, progress bar with a count knob, countdown callout, one slot per item, live total and savings, and one button that adds the whole box to the cart and applies the size's discount code.

It's built to drop into **any** Online Store 2.0 theme with no other changes. The discount itself is a normal Shopify discount code the merchant creates in admin. The section never creates discounts.

```
sections/bundle-builder.liquid          The product. Markup, CSS, JS and schema in one file.
extras/bundle-builder-cart-savings.liquid  Optional snippet: "You're saving $X" in the theme's cart.
demo/page.bundle.json                   Example page template (demo store handles)
demo/build_product_images.py            Draws the 12 demo packshots (Pillow) into demo/product-images/
demo/build_products_csv.py              Writes demo/products.csv for Products > Import
demo/product-images/                    12 transparent PNG packshots (fictional brand BOXFUL)
```

## Installing into a theme

Ask the human for: the store, which theme (always an unpublished copy first), the box sizes and discounts they want, and which collection or products go in the box.

1. **Copy the section.** `sections/bundle-builder.liquid` into the theme's `sections/` folder, unchanged.
2. **Discount codes (human does this in admin).** One per box size: **Discounts > Amount off products**, percentage = the size's Discount setting, applies to the box collection (or specific products), **Minimum quantity of items** = the box size. Shopify CLI has no discount commands and a theme can't create discounts, so you can't do this step. Tell the human exactly what to create (see the table in README step 2) and check for conflicts (next section).
3. **Page template.** Create `templates/page.bundle.json`. Minimal version:
   ```json
   {
     "sections": {
       "main": {
         "type": "bundle-builder",
         "blocks": {
           "size_4": { "type": "size", "settings": { "size": 4, "discount": 10, "code": "BUNDLE4", "default": true } },
           "size_6": { "type": "size", "settings": { "size": 6, "discount": 15, "code": "BUNDLE6", "badge": "Most popular" } },
           "size_8": { "type": "size", "settings": { "size": 8, "discount": 20, "code": "BUNDLE8", "badge": "Best value" } },
           "cat_all": { "type": "category", "settings": { "title": "Best sellers", "collection": "build-your-box" } }
         },
         "block_order": ["size_4", "size_6", "size_8", "cat_all"],
         "settings": { "after_add": "cart" }
       }
     },
     "order": ["main"]
   }
   ```
   `collection` takes a collection **handle**, `products` takes product **handles**. [`demo/page.bundle.json`](demo/page.bundle.json) is a full example with prebuilt bundles and custom styling.
4. **Push to an unpublished theme:** `shopify theme push --unpublished --theme "With bundle builder"`, or `--only sections/bundle-builder.liquid --only templates/page.bundle.json` against an existing theme ID. Ask the human before touching the live theme (`--allow-live`).
5. **The human creates the page:** **Online Store > Pages > Add page**, Theme template `bundle`. The template dropdown only lists templates from the **published** theme. To preview on an unpublished theme before that, open any existing page with `?view=bundle&preview_theme_id=<theme id>` (for example `/pages/contact?view=bundle&preview_theme_id=123`).
6. **Pick the after-add behavior** for this theme (see [Theme integration](#theme-integration)). `cart` works everywhere.
7. **Optional cart savings line.** Copy `extras/bundle-builder-cart-savings.liquid` to the theme's `snippets/` and add `{% render 'bundle-builder-cart-savings' %}` right after the cart total. Horizon: `snippets/cart-summary.liquid`, after the `cart-totals__total` element (covers drawer and cart page). Dawn family: `snippets/cart-drawer.liquid` and `sections/main-cart-footer.liquid`, after the `.totals` block. Elsewhere: search the cart templates for `cart.total_price`. Make sure the drawer re-renders that markup after an add (it does in Horizon and Dawn, since both re-fetch their cart sections).
8. Run the [checks](#before-you-hand-back).

### Discount conflicts (check this every install)

The box codes are **product discounts**. In this order, these are the usual reasons a box code doesn't apply:

- **An automatic discount that doesn't combine.** Shopify keeps whichever saves more, and the code shows `"applicable": false` in `/cart.js` `discount_codes`. Fix: set Combinations on both discounts, or pause the automatic one. Ask the human; never pause discounts without asking.
- **Percent mismatch.** The section's savings line uses the size block's Discount setting. If the code's percent differs, the shopper sees one number and pays another.
- **Products outside the code's collection**, or a minimum quantity that doesn't match the size.

How to debug it from a browser on the storefront: fill a box, add it, then `await (await fetch('/cart.js')).json()` and read `discount_codes` and each item's `line_level_discount_allocations`.

## Hard rules when changing the section

These keep it portable. Breaking one usually works in the theme you're testing and fails in every other theme.

1. **Stay one file.** CSS in `{% stylesheet %}`, JS in `{% javascript %}`. No new files in `assets/` or `snippets/` for core behavior. `{% stylesheet %}` and `{% javascript %}` can't contain Liquid; pass values in through CSS variables or `data-` attributes on `<bundle-builder>`. (`extras/` is for optional add-ons the merchant installs separately.)
2. **No theme dependencies for core behavior.** Don't use a theme's classes (`page-width`, `color-scheme-1`), CSS variables (`--color-foreground`) or JS (`publish()`, theme components). Theme-specific hooks are allowed only as optional extras, feature-detected, like the branches in `openThemeCart()` and `notifyTheme()`.
3. **Prefix everything.** Classes `bbx__*` (BEM) and modifiers `bbx--*`. Data attributes `data-bbx-*`. CSS variables `--bbx-*`. Custom element `<bundle-builder>`. Events `bundle-builder:*`. Never style bare tags; every rule is scoped under `.bbx`.
4. **Size text in `em`.** Themes set different root sizes (Dawn uses 62.5%, so 1rem = 10px; Horizon uses 16px). `rem` breaks in one or the other. Use `px` only for fixed UI: borders, icons, hit targets, gaps.
5. **Colors come from settings.** Use the `--bbx-*` color variables (see [Branding](#branding-and-the-color-system)). Don't hard-code colors except neutral overlays and the error red.
6. **Every shopper-facing string is a setting** (schema `text`, under the "Text and translations" header), passed to JS as `data-label-*` on the root and read with `this.dataset.label*`. Placeholders use `[brackets]`. The aria-labels built in JS (`Remove {title}`, `Add one {title}`) are the one exception so far.
7. **Guard the element definition:** `if (customElements.get('bundle-builder')) return;`. `{% javascript %}` runs once per page even if the section appears twice.
8. **Match Shopify's discount math.** Savings = for each product line, `floor(line price × percent / 100)`, summed. Shopify rounds each line down; rounding the total instead drifts by a few cents.
9. **Defend against theme tag styles.** Themes style bare `button`, `h2`, `li` and `:focus`. The resets at the top of the stylesheet (`.bbx :where(button)`, `.bbx :where(h2, h3, p)`, `.bbx :where(ul, li)`) neutralize them at class-level specificity, and the component rules after them win. New buttons and lists inherit this; keep new rules below the resets, and give every new button its own padding, background and border.
10. **Keep keyboard focus.** When an action hides the focused control (+ Add turns into a stepper, × removes a slot), move focus to its replacement in `onClick`. `.bbx :focus-visible` draws the ring; don't remove it.

## How the file is laid out

Top to bottom (line numbers drift; search for the comments):

1. **Liquid setup** (`{%- liquid -%}`): splits `section.blocks` into `sizes`, `cats` and `bundle_presets`, finds the default size, builds the custom font stack.
2. **Font faces:** a `<style>` with `font_face` output, only when **Use a custom font** is on.
3. **Root `<bundle-builder>`:** every visual setting as an inline CSS variable (`--bbx-bg`, `--bbx-ink`, `--bbx-radius`, `--bbx-btn-radius`, `--bbx-border`, `--bbx-cols-d`, `--bbx-sticky`, ...), plus cart routes, money format, behavior flags and every label as `data-*`. Modifier classes: `bbx--upper`, `bbx--sticky-nav`, `bbx--fit-contain|cover`.
4. **Header and category nav:** `.bbx__nav` with one `a.bbx__pill[data-bbx-nav]` per category, linking to `#bbx-{section.id}-{block.id}`.
5. **Builder panel** `aside.bbx__panel[data-bbx-panel]` (first in the DOM so it's above the catalog on mobile): size buttons `[data-bbx-size]`, progress `[data-bbx-progress]` with `[data-bbx-count]`/`[data-bbx-target]` knobs, status callout `[data-bbx-status]`, slots `ul[data-bbx-slots]`, `[data-bbx-clear]`, totals `[data-bbx-compare]`/`[data-bbx-price]`/`[data-bbx-saving]`, `button[data-bbx-cta]`, `[data-bbx-error]`.
6. **Catalog** `[data-bbx-catalog]`: the prebuilt bundles strip (`button[data-bbx-preset]` with its products as JSON in `data-items`), then one `section.bbx__cat[data-bbx-cat]` per category with `li.bbx__card[data-bbx-card]` cards. Each card carries `data-variant-id`, `data-price` (cents), `data-title`, `data-image`, `data-available` and contains `[data-bbx-add]`, `[data-bbx-stepper]` (`[data-bbx-dec]`, `[data-bbx-qty]`, `[data-bbx-inc]`).
7. **Mobile dock** `[data-bbx-dock]`: `[data-bbx-view-box]` (count, "View box", status) and a second `[data-bbx-cta]`. Hidden at 990px and up.
8. **`{% stylesheet %}`**, mobile first. Breakpoints: 750px (grid gaps, panel padding, pill row stops scrolling sideways) and 990px (two columns with the sticky panel, dock hidden).
9. **`{% javascript %}`**: the `BundleBuilder` class.
10. **`{% schema %}`**: settings grouped Content, Colors, Style, Typography, Layout, Box behavior, Text and translations; blocks `size`, `category`, `preset`; three section presets (the three looks).

### State and rendering

All state lives on the element:

- `this.slots`: array of variant ID strings in the order they were added. Duplicates allowed. This is the box.
- `this.sizeIndex`: index into `this.sizeButtons`. `this.size`, `this.discount` and `this.code` read from that button's data attributes.
- `this.products`: `Map` of variant ID → `{ id, title, price, image, available }`, built from the cards plus every preset's `data-items` (so presets can include products that aren't in any category).
- `this.activePreset`: the preset button to highlight, cleared as soon as the box stops matching it.

Every action changes state, then calls `render()`, which redraws everything from state: size buttons, progress, status text, slots (diffed in place so images don't flash), cards (qty, stepper vs add button, disabled when nothing more can be added), totals and savings, both CTAs, the dock. Then it calls `save()` (sessionStorage, keyed by section ID and path). Never update the DOM from an action directly; change state and render.

### JavaScript (`BundleBuilder`)

| Method | Job |
|---|---|
| `connectedCallback` / `disconnectedCallback` | Build `products`, read the default size, `restore()`, wire listeners and observers |
| `save` / `restore` | sessionStorage `{ size, slots }`. Restore drops products that are gone or sold out |
| `onClick` | One delegated handler for every `data-bbx-*` control |
| `onBlockSelect` | Theme editor: selecting a size block selects that size; selecting a preset block applies it |
| `selectSize` | Switch size, trim slots from the end if the new size is smaller |
| `add` / `removeOne` | Add or remove one of a variant. `add` moves up to the next size when full and `auto_upgrade` is on |
| `applyPreset` | Pick the preset's size (or the closest bigger one), fill the slots by repeating its products |
| `nextSizeIndex` / `canAddMore` | Next bigger size, and whether + buttons should be enabled |
| `render` / `renderSlots` / `buildSlot` | See above |
| `money` | Formats cents in the shopper's currency. Liquid renders `123456789 \| money` into `data-money-sample` (presentment currency, so Markets work) and JS reads the symbol, separators and decimals from it |
| `addBox` | The cart flow, below |
| `applyCode` | `POST /cart/update.js { discount }` with this size's code (or none), dropping other sizes' codes and keeping unrelated codes. Returns `false` when the code didn't end up `applicable` |
| `fetchCart` / `toStandardCart` | Read `/cart.js`, convert to the Shopify standard-events cart shape |
| `notifyTheme` | Cart icon refresh for Dawn-style themes, `publish('cart-update')`, and the `bundle-builder:cart:added` event |
| `openThemeCart` | After-add drawer opening, per theme family. **Add support for more themes here** |
| `watchDock` | IntersectionObserver: dock shows while the catalog is on screen and the panel's button isn't |
| `watchNav` / `revealPill` | Highlights the pill for the category in view and scrolls the pill row sideways on phones |
| `watchSticky` / `measureSticky` / `headerBottom` / `stickyHeaderHeight` | Sticky header detection, below |
| `scrollToBox` / `scrollToCatalog` / `pulseStatus` | Jumps and the little shake on the status callout |

### Cart flow (`addBox`)

1. `this.adding` blocks a second run (double clicks, Enter held down). Group `slots` into `items: [{ id, quantity }]`.
2. If **After adding the box** is `drawer`: create a promise and dispatch `shopify:cart:lines-update` (`action: 'add'`, `lines` with `gid://shopify/ProductVariant/{id}` merchandise IDs, `promise`) from the button. Themes on Shopify's standard cart events (Horizon) refresh their cart from that promise.
3. `POST {routes.cart_add_url}.js` with `{ items, sections: 'cart-icon-bubble' }`. **This is the only step that can fail the box.** On failure: reject the promise, show Shopify's own message (like a stock limit) or the generic error label, keep the box.
4. Everything after a successful add is wrapped so it can't report failure (a retry would add the box twice): `applyCode(code)`, `GET /cart.js`, resolve the promise with `{ cart: toStandardCart(cart), detail: { itemCount } }`, `notifyTheme()`.
5. Empty the box and `save()` before any redirect, so the Back button doesn't restore a box that's already in the cart. A `pageshow` listener also resets the buttons when the page comes back from the back/forward cache.
6. Then by setting: `cart` → `routes.cart_url`; `checkout` → `{root}/checkout`; `drawer` → `openThemeCart()` and "Added to cart!" for 2.5 seconds.
7. If the code didn't apply, show the `label_code_error` notice under the button (not an error; the box is in the cart).

## Theme integration

| Theme family | After-add drawer | Cart icon count | How |
|---|---|---|---|
| **Horizon** (Horizon, and the 2025 themes built on it) | Opens, even when the theme's own auto-open setting is off | Updates | Standard `shopify:cart:lines-update` event, then `theme-drawer#cart-drawer`.`open()`. Tested on the demo store |
| **Dawn** (Dawn, Refresh, Sense, Craft, Studio, Taste, Crave, Colorblock, Ride, Origin, Spotlight, Publisher) | Opens | Updates | Fetches the drawer's own sections (`?sections=cart-drawer,cart-icon-bubble`) after the discount is applied and calls `cart-drawer`.`renderContents()`. Written against Dawn's current source (`assets/cart-drawer.js`); not yet run on a live Dawn store, so test it on the first Dawn install. If the theme's cart type is the **notification** popup instead of a drawer, nothing opens; use `cart` |
| **Everything else** | Doesn't open | Updates on next page load | Use `after_add: "cart"`, or add a branch (below) |

### Supporting another theme's cart

1. Find what the theme's own product form does after adding to cart. Search its `assets/` for `cart/add`, `cart:refresh`, `cart:open`, `renderContents`, `CartDrawer` or `ajaxProduct`. Most themes either call a method on a drawer element or dispatch a document event.
2. Add a branch to `openThemeCart()` that does the same thing, **feature-detected** so it does nothing in other themes. Return after it runs so later branches don't fire. Examples of the shape:
   ```js
   // Theme X: listens for a document event and re-renders its own drawer
   if (document.querySelector('cart-drawer-x') && window.ThemeX?.cart) {
     document.dispatchEvent(new CustomEvent('cart:refresh', { bubbles: true }));
     document.dispatchEvent(new CustomEvent('cart:open'));
     return;
   }
   ```
3. Re-render after the discount is applied (`openThemeCart` runs after `applyCode`), or the drawer shows pre-discount prices.
4. Don't remove existing branches. Add a row to the table above and to the README theme table.

### Sticky header detection

The category bar sticks at `top: var(--bbx-offset)` and the desktop panel at `--bbx-offset + --bbx-nav-h + --bbx-sticky`. JS fills these in:

- `headerBottom()` runs on every scroll frame. It looks at the elements under the top center of the screen and returns the bottom edge of the first `position: fixed|sticky` ancestor outside this section (ignoring anything taller than 40% of the screen, like drawers). That handles headers that hide on scroll down and show on scroll up.
- `stickyHeaderHeight()` runs once at load and scans the top 30% of the screen for the same, to get `--bbx-header-h`. Category jumps and "View box" use `max(--bbx-offset, --bbx-header-h)` in `scroll-margin-top`, so they land below the header even from the very top of the page before the header has stuck.
- Scroll is listened for on `document` in the **capture** phase. Horizon scrolls a `.page-wrapper` element, not the window, so a `window` scroll listener never fires there.

If a theme has something unusual pinned to the top (a fixed announcement bar, a cookie banner), detection will include it, which is usually what you want. If it gets a theme wrong, the merchant can raise **Builder panel gap from top**; for a hard fix, add a feature-detected exclusion in `headerBottom()`.

`position: sticky` stops working if any ancestor has `overflow: hidden|auto|scroll|clip` on the scrolling axis. If the bar or panel doesn't stick in some theme, check the section's ancestors in devtools. The fix belongs in the theme (or a scoped override on that theme's wrapper), not in this file. The page still works without sticking.

The mobile dock is `position: fixed`. If an ancestor has `transform`, `filter` or `contain` (some themes animate sections in with a transform), the dock pins to that ancestor instead of the screen. Same fix: remove the effect on the bundle page's section wrapper in the theme.

Stacking: the sticky bar is `z-index: 2` (above cards, below theme headers and their menus, which are usually 3+). The dock is `z-index: 10`. If a theme's header dropdowns or a chat widget overlap wrongly, adjust these two numbers only.

## Branding and the color system

Merchants rebrand through settings. When you're asked to "make it match my brand", change settings in the template JSON (or tell the human which to set), not the CSS.

| Setting | CSS variable | Used for |
|---|---|---|
| `color_bg` | `--bbx-bg` | Section background, sticky bar background, preset button background |
| `color_ink` | `--bbx-ink` | All text, borders, buttons, progress fill, knobs, step numbers |
| `color_button_text` | `--bbx-btn-fg` | Text on `--bbx-ink` (buttons, active pills, knobs); idle CTA background |
| `color_selected` | `--bbx-selected` | Cards in the box, savings badge, full-box callout, full knob ring |
| `color_panel` | `--bbx-panel-bg` | Builder panel and mobile dock |
| `color_card` | `--bbx-card` | Product cards |
| `radius` | `--bbx-radius` | Cards; panel is +6px, slots ×0.75 |
| `button_shape` | `--bbx-btn-radius` | 999px / 12px / 0. Buttons, pills, size picker, badges, callouts |
| `border_width` | `--bbx-border` | Every ink border |
| size block `badge_bg` / `badge_color` / `badge_text` | `--bbx-badge-bg` / `--bbx-badge-fg` | That size's badge. `badge_bg` (gradient-capable) wins over `badge_color` |

Derived in CSS with `color-mix()`, so they follow the four main colors automatically: `--bbx-track` (progress track), `--bbx-line` (rules), `--bbx-soft` (empty slots, status callout). Don't add settings for these.

Contrast: `--bbx-ink` on `--bbx-bg`, `--bbx-card`, `--bbx-panel-bg` and `--bbx-selected` all carry text, and `--bbx-btn-fg` sits on `--bbx-ink`. Check all of those reach 4.5:1 when you pick a palette.

To add a fourth ready-made look, add an entry to `presets` in the schema with the color and style settings plus the same four blocks the other presets have.

## Common changes

- **New setting:** add it to `{% schema %}` under the right header. Read it in Liquid as `s.<id>`. For CSS, add a `--bbx-*` inline variable on the root; for JS, a `data-*` attribute. Use `visible_if` for settings that only matter when another is on (see `font`).
- **New shopper-facing text:** a `text` setting under "Text and translations" with a default, passed as `data-label-*`, read via `this.dataset.label*` and filled with the `fmt()` helper inside `render()` for `[placeholders]`.
- **Subscriptions (a "one-time / subscribe" step):** read each product's `selling_plan_groups` in Liquid, add a step 3 with radio buttons in the panel, store the choice in state, and send `selling_plan` per item in `addBox`. Note that most discount codes don't apply to subscription lines unless the code allows it.
- **Option pickers on cards (sizes, flavors):** render the variants as JSON on the card, add a small `<select>` or chips, and swap the card's `data-variant-id`, `data-price` and `data-image` on change. Slots and totals already key off variant IDs, so nothing else changes.
- **Group the box in the cart:** add line item properties in `addBox`, like `properties: { _bundle: 'Box of 6' }`. Underscore properties are hidden at checkout. Lines with different properties won't merge with the same product bought on its own.
- **Different slot layout:** `renderSlots` puts 4 per row, or 3 when the size divides by 3 but not 4 (`.is-cols-3`). Change the flex-basis in `.bbx__slot`.
- **More than 4 sizes:** raise `limit` on the `size` block. The size picker is a CSS grid that shares the width equally, so 5+ sizes need smaller text or a scrollable row.

## Gotchas

- Products with options (sizes, colors) add their first available variant, and the card and slot show that variant's name. There's no picker yet (see Common changes).

- Shopify CLI can't create products, collections, files or discounts. Those go through admin (Products > Import for a CSV, Content > Files for images).
- `image_picker` and Files URLs only work for files already in the store. CSV `Image Src` must be a public URL; files in Content > Files are served at `https://<store>/cdn/shop/files/<filename>`.
- `product_list` settings cap at `limit` (50 on categories, 24 on presets).
- The template dropdown on pages only lists templates from the published theme. Use `?view=bundle` to preview.
- After adding the section in the theme editor, a merchant may need to save and refresh before the JS runs in the preview.
- `{% javascript %}` runs once per page. Per-instance state lives on the element, and sessionStorage is keyed by section ID, so two builders on one page don't collide.
- `color-mix()` needs a 2023-or-newer browser. Older browsers fall back to the base colors for the derived tints.

## Before you hand back

1. **Schema is valid JSON:**
   ```bash
   python3 -c "import re,json;s=open('sections/bundle-builder.liquid').read();json.loads(re.search(r'{% schema %}(.*?){% endschema %}',s,re.S).group(1));print('ok')"
   ```
2. **JS parses:**
   ```bash
   python3 -c "import re;s=open('sections/bundle-builder.liquid').read();open('/tmp/bbx.js','w').write(re.search(r'{% javascript %}(.*?){% endjavascript %}',s,re.S).group(1))" && node --check /tmp/bbx.js
   ```
3. **Theme check passes** inside a full theme (it needs `locales/` and `config/`): copy the section into a pulled theme and run `shopify theme check`. Only look at offenses for `bundle-builder.liquid`.
4. **Push succeeds without schema errors.** Shopify rejects things theme check misses (range settings need at least 3 steps, option labels max 50 characters).
5. **Manual test on a dev store**, desktop and a phone-width window:
   - Each size: fill the box, watch the countdown, totals and savings; overfill to see it move up a size; pick a smaller size and see it trim.
   - Remove with ×, with −, and with Clear all. Reload: the box comes back.
   - Each prebuilt bundle fills the right size.
   - Scroll: the category bar sticks under the header, the active pill follows, the desktop panel stays below the bar. Click each pill from the top of the page.
   - Phone width: the dock appears over the products, "View box" jumps back to the slots.
   - Add the box: every item lands in the cart, `/cart.js` shows the code with `"applicable": true`, and the cart total matches the section's total to the cent.
6. **Keep the docs in sync:** new settings or behavior go in README.md (for merchants) and this file (for agents).
