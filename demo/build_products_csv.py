"""Generate a Shopify product import CSV for the demo snack catalog (fictional brand BOXFUL).

Images are the packshots from build_product_images.py, uploaded to the store's Content > Files.
Files are served at <store>/cdn/shop/files/<filename>, which is what Image Src points at.
Run: python3 demo/build_products_csv.py [store-domain]  ->  demo/products.csv
"""
import csv
import sys
from pathlib import Path

STORE = sys.argv[1] if len(sys.argv) > 1 else "lookbook-build.myshopify.com"
IMG = f"https://{STORE}/cdn/shop/files/{{}}.png"
VENDOR = "BOXFUL"

# handle, title, type, price, tags, description
PRODUCTS = [
    ("grapefruit-sparkling-soda", "Grapefruit Sparkling Soda", "Sparkling Soda", 9.75, "build-your-box, drinks, bestseller",
     "Tart pink grapefruit with a bright, dry finish. 4 cans, 12 fl oz each, zero sugar."),
    ("lime-sparkling-soda", "Zesty Lime Sparkling Soda", "Sparkling Soda", 9.75, "build-your-box, drinks",
     "Squeezed-lime snap with extra fizz. 4 cans, 12 fl oz each, zero sugar."),
    ("peach-mango-sparkling-soda", "Peach Mango Sparkling Soda", "Sparkling Soda", 9.75, "build-your-box, drinks, bestseller",
     "Ripe peach and mango, like summer in a can. 4 cans, 12 fl oz each, zero sugar."),
    ("wild-berry-sparkling-soda", "Wild Berry Sparkling Soda", "Sparkling Soda", 9.75, "build-your-box, drinks",
     "Blackberry, raspberry and a little tang. 4 cans, 12 fl oz each, zero sugar."),
    ("sea-salt-popcorn", "Sea Salt Popcorn", "Popcorn", 5.95, "build-your-box, snacks, popcorn, bestseller",
     "Air-popped and finished with flaky sea salt. Simple, crunchy, gone too fast."),
    ("kettle-corn-popcorn", "Kettle Corn Popcorn", "Popcorn", 5.95, "build-your-box, snacks, popcorn",
     "The fair-food classic: lightly sweet, lightly salty, all crunch."),
    ("white-cheddar-popcorn", "White Cheddar Popcorn", "Popcorn", 5.95, "build-your-box, snacks, popcorn, bestseller",
     "Aged white cheddar in every bite. You will lick your fingers."),
    ("chili-lime-popcorn", "Chili Lime Popcorn", "Popcorn", 5.95, "build-your-box, snacks, popcorn",
     "Smoky chili and bright lime with a slow, friendly heat."),
    ("chocolate-chip-protein-bars", "Chocolate Chip Protein Bars", "Protein Bars", 19.95, "build-your-box, snacks, bars, bestseller",
     "Chewy, cookie-dough style bars with real chocolate chips. 12 bars, 12g protein each."),
    ("peanut-butter-protein-bars", "Peanut Butter Protein Bars", "Protein Bars", 19.95, "build-your-box, snacks, bars",
     "Roasted peanut butter with a chocolate drizzle. 12 bars, 12g protein each."),
    ("birthday-cake-protein-bars", "Birthday Cake Protein Bars", "Protein Bars", 19.95, "build-your-box, snacks, bars",
     "Vanilla cake, sprinkles and frosting vibes. 12 bars, 12g protein each."),
    ("cookies-and-cream-protein-bars", "Cookies & Cream Protein Bars", "Protein Bars", 19.95, "build-your-box, snacks, bars",
     "Crushed chocolate cookies in a creamy base. 12 bars, 12g protein each."),
]

HEADERS = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Variant SKU", "Variant Grams",
    "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
    "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price",
    "Variant Requires Shipping", "Variant Taxable", "Image Src", "Image Position",
    "Image Alt Text", "Status",
]


def rows():
    for handle, title, ptype, price, tags, desc in PRODUCTS:
        yield {
            "Handle": handle,
            "Title": title,
            "Body (HTML)": f"<p>{desc}</p>",
            "Vendor": VENDOR,
            "Type": ptype,
            "Tags": tags,
            "Published": "TRUE",
            "Option1 Name": "Title",
            "Option1 Value": "Default Title",
            "Variant SKU": f"BX-{handle.upper()}",
            "Variant Grams": 600,
            "Variant Inventory Tracker": "shopify",
            "Variant Inventory Qty": 100,
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant Price": f"{price:.2f}",
            "Variant Compare At Price": "",
            "Variant Requires Shipping": "TRUE",
            "Variant Taxable": "TRUE",
            "Image Src": IMG.format(handle),
            "Image Position": 1,
            "Image Alt Text": title,
            "Status": "active",
        }


if __name__ == "__main__":
    out = Path(__file__).parent / "products.csv"
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(rows())
    print(f"Wrote {out} ({len(PRODUCTS)} products)")
