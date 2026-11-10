# Build-Your-Own Bundle for Shopify

A "build your box" page for any Shopify theme. Shoppers pick a box size (4, 6 or 8), fill it with products, watch the savings grow, and add the whole box to the cart in one click. Bigger boxes get bigger discounts.

It's one file. No app, no monthly fee, and you can install it without touching code.

**Using Claude Code, Cursor or another AI coding tool?** Point it at this repo and say what you want, like "install this in my theme", "make it match my brand colors" or "add a subscription option". [AGENTS.md](AGENTS.md) tells it how everything works and how to change it without breaking it in other themes.

## What it does

- **Box sizes with their own discount.** Each size is a pill (4 Pack, 6 Pack, 8 Pack) with "Save 10%" underneath and an optional badge like "Most popular" or "Best value".
- **A live countdown.** "Add 2 more to unlock 10% off" sits under the progress bar and the button reads "Add 2 more". When the box is full it nudges the next size: "Box full! Add 2 more to unlock 15% off with the 6 Pack".
- **Every slot visible.** Empty slots show a +, filled slots show the product with an × to remove it. A small "Clear all" link empties the box.
- **Live total.** Crossed-out original price, discounted price, and "You're saving $8.40". The math matches Shopify's checkout to the cent.
- **Product categories with jump links.** Group products (Best sellers, Drinks, Snacks...) and shoppers jump between them with pill links that stay on screen while they scroll.
- **Prebuilt bundles.** One-click buttons like "All star" or "Discovery kit" fill the box for the shopper. They can swap anything after.
- **One click to add the whole box.** The matching discount code is applied to the cart automatically.
- **Made for phones.** On mobile a bar at the bottom shows "2/4" and the add button while shoppers browse. Tap it to jump back up and review the box.
- **Remembers the box** if the shopper reloads or comes back to the page in the same visit.
- **Easy to rebrand.** Four colors, corner roundness, button shape, border width and font, all in the theme editor. Three ready-made looks to start from.

## Before you start

You need:

- A Shopify theme that supports sections on every page ("Online Store 2.0"). Every free Shopify theme since 2021 does, including Horizon and Dawn.
- The products you want in the box. Single-variant products work best (one flavor, one size). See [Products with options](#products-with-options).

**Tip:** install on a copy of your theme first. In **Online Store > Themes**, click **...** next to your theme and choose **Duplicate**. Try it there, then publish the copy when you're happy.

## Install it (about 10 minutes, no coding)

### Step 1: Add the section file

1. Open [`sections/bundle-builder.liquid`](sections/bundle-builder.liquid) here on GitHub and click **Copy raw file** (the two-squares icon at the top right of the file).
2. In your Shopify admin, go to **Online Store > Themes**. Next to your theme, click **...** then **Edit code**.
3. In the file list on the left, find the **Sections** folder and click **Add a new section**.
4. Name it `bundle-builder` and pick **Liquid** if it asks.
5. Delete everything in the new file, paste what you copied, and click **Save**.

### Step 2: Create the discount codes

The section applies a discount code when the box goes in the cart. Shopify does the actual discounting, so you create one code per box size.

Go to **Discounts > Create discount > Amount off products** and make one code for each size:

| Code | Value | Applies to | Minimum purchase requirements |
|---|---|---|---|
| `BUNDLE4` | 10% | The collection your box products are in | Minimum quantity of items: 4 |
| `BUNDLE6` | 15% | Same collection | Minimum quantity of items: 6 |
| `BUNDLE8` | 20% | Same collection | Minimum quantity of items: 8 |

Use any code names and percentages you like. Two things matter:

- **The percent must match** the Discount you set on that box size in the section. That's how "You're saving $X" matches checkout.
- **Watch out for automatic discounts.** If your store runs an automatic discount (like "10% off orders over $100") that doesn't combine with product discounts, Shopify gives the shopper whichever saves more, and your box code can lose. Either let them combine (under **Combinations** on both discounts) or pause the automatic one.

A collection just for box products (say "Build Your Box") keeps the discount off everything else in the cart.

### Step 3: Make the page

1. Go to **Online Store > Themes** and click **Customize**.
2. In the dropdown at the top, choose **Pages**, then **Create template**. Name it `bundle` and click **Create template**.
3. Click **Add section** and choose one of the **Bundle builder** options (see [Make it yours](#make-it-yours) for the three looks). Remove the page's default sections if you don't want them.
4. Click **Save**.
5. Go to **Online Store > Pages > Add page**. Give it a title (like "Build your box"), set **Theme template** to `bundle`, and save.

Your page is live at `yourstore.com/pages/build-your-box` (or whatever you named it). Link it from your menu, emails and ads.

### Step 4: Set up your box

In the theme editor, open the Bundle builder section. It's built from blocks:

**Box size** (up to 4). For each one:
- **Items in the box:** 4, 6, 8, or whatever you sell.
- **Discount:** the percent off. Must match the code from step 2.
- **Discount code:** the code from step 2, like `BUNDLE4`.
- **Badge:** optional, like "Most popular". Pick its colors right below.
- **Selected when the page loads:** turn this on for the size you want shoppers to start with.

**Product category** (as many as you like). Each one is a group of products with its own heading and jump link:
- **Title:** like "Best sellers" or "Sparkling soda".
- **Collection** or **Or pick products:** where the products come from. Picked products override the collection.

**Prebuilt bundle** (optional, up to 6). A button that fills the box in one click:
- **Name:** like "All star".
- **Box size:** which size it fills. Use one of your box sizes.
- **Products:** what goes in. If you pick fewer products than the box holds, they repeat in order (3 products in a 6 Pack = 2 of each).

## Make it yours

When you click **Add section**, you can start from three looks:

| Look | Feel |
|---|---|
| **Bundle builder** | Bright lavender and purple with a cyan highlight. Bold and playful. |
| **Bundle builder: clean** | White, black and a yellow highlight. Square-ish corners, thin borders. |
| **Bundle builder: earthy** | Cream, forest green and apricot. Soft and natural. |

Then make it match your brand in the section settings:

**Colors.** Four colors do most of the work:

| Setting | What it colors |
|---|---|
| Page background | Behind everything |
| Brand color | Text, borders, buttons, the progress bar |
| Text on brand color | Button labels and anything on the brand color (usually white) |
| Highlight | Products in the box, the savings badge, the full-box message |

Builder panel background and Product card background are there if you want those areas to differ from the page. The softer lines and tints are mixed from your colors automatically, so there's nothing else to tune.

**Style.** Corner roundness (0 for sharp, 32 for very round), button shape (pill, rounded or square) and border width (1 to 4px).

**Typography.** The section uses your theme's font by default. Turn on **Use a custom font** to pick another. **Uppercase titles and buttons** gives the bold packaging look; turn it off for something softer.

**A good recipe:** use your logo's darkest color as Brand color, your background color as Page background, and your loudest accent as Highlight. Check that the brand color is easy to read on the background.

## Change the words

Every word shoppers see is in **Text and translations** at the bottom of the section settings. Words in [brackets] fill in automatically:

- `[count]`: how many items (left to add, or in the box)
- `[percent]`: the discount
- `[amount]`: money saved
- `[price]`: the box total after the discount
- `[size]`: a box size name, like "6 Pack"
- `[name]`: a prebuilt bundle's name

For example, "Add [count] more to unlock [percent]% off" shows as "Add 2 more to unlock 10% off".

## Show savings in the cart

Optional, and it takes a few minutes in the code editor. This adds a "You're saving $X" badge under the cart total, counting every discount plus any compare-at markdowns.

1. In **Edit code**, open the **Snippets** folder, click **Add a new snippet**, name it `bundle-builder-cart-savings`, and paste in [`extras/bundle-builder-cart-savings.liquid`](extras/bundle-builder-cart-savings.liquid).
2. Add this line where you want the badge to show:
   ```liquid
   {% render 'bundle-builder-cart-savings' %}
   ```
   - **Horizon** and its sister themes: in `snippets/cart-summary.liquid`, right after the "Estimated total" line. That one spot covers both the cart drawer and the cart page.
   - **Dawn** and Dawn-based themes: in `snippets/cart-drawer.liquid` (cart drawer) and `sections/main-cart-footer.liquid` (cart page), right after the block with `class="totals"`.
   - **Other themes:** search the cart files for `cart.total_price` and put it just below that.

You can change the wording and colors: `{% render 'bundle-builder-cart-savings', label: 'Box savings: [amount]', background: '#FFE55C', color: '#111111' %}`.

## Works with your theme

Building the box, the discount and adding to cart work in every Online Store 2.0 theme. What happens right after "Add box to cart" depends on the **After adding the box** setting and your theme:

| Theme | "Stay on the page and open the cart drawer" |
|---|---|
| Horizon and its sister themes | Cart drawer opens with the box in it (tested) |
| Dawn and Dawn-based themes (Refresh, Sense, Craft, Studio, Taste, Crave, Colorblock, Ride, Origin, Spotlight, Publisher) | Cart drawer opens with the box in it (built from Dawn's code, not yet tested on a live Dawn store; your theme's cart type must be set to Drawer) |
| Other themes | Shopper stays on the page and the button says "Added to cart!". The cart icon count catches up on the next page load |

If your theme isn't in the first two rows, set **After adding the box** to **Go to the cart page**. That works everywhere. Or ask your AI coding tool to "connect the bundle builder to my theme's cart drawer" and point it at [AGENTS.md](AGENTS.md).

**For developers:** after every add, the section fires `bundle-builder:cart:added` on `document` with the full `/cart.js` response in `event.detail.cart`.

## Products with options

Each product card adds the product's first available variant and shows its name under the title (like "Small / Black"). That's perfect for one-flavor, one-size products. If a product has options (sizes, colors), either split each option into its own product for the box, or ask your AI coding tool to add an option picker to the cards (AGENTS.md covers how).

## Troubleshooting

**"Bundle builder" isn't in the Add section list.**
Check the file is in the **Sections** folder and named exactly `bundle-builder.liquid`.

**The `bundle` template isn't in the page's Theme template dropdown.**
The dropdown only shows templates from your **published** theme. Publish the theme copy, or build the template on your live theme too.

**Checkout doesn't apply the box discount.**
Check, in order: the code on the Box size block matches the code in **Discounts** exactly; the code is active; the box products are in the collection the code applies to; the minimum quantity matches the box size; and no automatic discount is beating it (see step 2).

**After adding, it says "the box discount couldn't be applied".**
The box is in the cart at full price. Same checklist as above: the code is mistyped, expired, outside its collection, or another discount is beating it.

**"You're saving" in the box is a few cents off checkout.**
The section rounds the way Shopify does (each product line rounds down). If it's off by more than a few cents, the Discount percent on the Box size block doesn't match the code.

**The category links or builder panel hide behind my header.**
The section measures your theme's sticky header automatically. If your theme does something unusual, raise **Builder panel gap from top** under Layout.

**A product is missing from the box options.**
Sold-out products show "Sold out" and can't be added. Draft products don't show at all.

## Try the demo

The `demo` folder has the snack catalog from the demo store: 12 products (sodas, popcorn and protein bars from a made-up brand, BOXFUL), their packshot images and the page template.

1. **Images:** in **Content > Files**, upload the 12 PNGs from [`demo/product-images`](demo/product-images). Keep the filenames.
2. **Products:** run `python3 demo/build_products_csv.py yourstore.myshopify.com`, then upload the new `demo/products.csv` in **Products > Import**. The script points each product at its image in your Files.
3. **Collection:** create a collection with the condition **Tag is equal to** `build-your-box`.
4. **Discounts:** create `BUNDLE4`, `BUNDLE6` and `BUNDLE8` as in step 2, applied to that collection.
5. **Template:** in **Edit code**, create a page template named `bundle` (choose JSON) and paste in [`demo/page.bundle.json`](demo/page.bundle.json). Then create a page that uses it.

The packshots are drawn by `demo/build_product_images.py`, so you can change flavors or colors and redraw them with `python3 demo/build_product_images.py` (needs Pillow).

## Install with Shopify CLI

If you use the CLI, copy `sections/bundle-builder.liquid` into your theme's `sections` folder and push to an unpublished theme:

```bash
shopify theme push --unpublished --only sections/bundle-builder.liquid
```

## License

MIT. Use it on your store or your clients' stores, change it, ship it. See [LICENSE](LICENSE).

Built with Claude Code on camera for the BS&Co YouTube channel.
