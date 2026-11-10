"""Render flat packshot PNGs for the demo catalog (fictional brand BOXFUL).

Three pack shapes: soda cans, popcorn bags, protein bar boxes. Transparent background so the
section's card colors show through, like real packshots.
Run: python3 demo/build_product_images.py  ->  demo/product-images/*.png
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).parent / "product-images"
SIZE = 1200
SS = 2  # supersample for smooth edges
BRAND = "BOXFUL"

FONT_DIRS = [Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/System/Library/Fonts/Supplemental")]
FONTS = {"black": ["Gilroy-Black.ttf", "Arial Black.ttf"], "bold": ["Gilroy-ExtraBold.ttf", "Arial Bold.ttf"]}


def font(kind, size):
    for name in FONTS[kind]:
        for d in FONT_DIRS:
            if (d / name).exists():
                return ImageFont.truetype(str(d / name), size * SS)
    return ImageFont.load_default()


def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4)) + (a,)


def mix(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def S(*v):
    return [x * SS for x in v]


def text_center(draw, cx, y, text, kind, size, fill, max_w):
    """Draw text centered at cx, shrinking to fit max_w. Returns bottom y."""
    while size > 10:
        f = font(kind, size)
        box = draw.textbbox((0, 0), text, font=f)
        if box[2] - box[0] <= max_w * SS:
            break
        size -= 2
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text((cx * SS - w / 2 - box[0], y * SS - box[1]), text, font=f, fill=fill)
    return y + h / SS


def shading(w, h, base, edge_dark=0.28, highlight=0.35, hl_pos=0.28):
    """Horizontal cylinder shading as an RGBA strip (w x h)."""
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    white, black = (255, 255, 255, 255), (0, 0, 0, 255)
    for x in range(w):
        t = x / max(1, w - 1)
        c = base
        edge = abs(t - 0.5) * 2
        c = mix(c, black, edge_dark * edge**3)
        hl = max(0, 1 - abs(t - hl_pos) / 0.09)
        c = mix(c, white, highlight * hl)
        d.line([(x, 0), (x, h)], fill=c)
    return img


def shadow(canvas, cx, cy, rx, ry, alpha=70):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(S(cx - rx, cy - ry, cx + rx, cy + ry), fill=(30, 10, 60, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(18 * SS))
    canvas.alpha_composite(layer)


def citrus(draw, cx, cy, r, rind, flesh):
    draw.ellipse(S(cx - r, cy - r, cx + r, cy + r), fill=rind)
    r2 = r * 0.86
    draw.ellipse(S(cx - r2, cy - r2, cx + r2, cy + r2), fill=(255, 255, 255, 255))
    r3 = r * 0.8
    draw.ellipse(S(cx - r3, cy - r3, cx + r3, cy + r3), fill=flesh)
    for i in range(8):
        draw.pieslice(S(cx - r3, cy - r3, cx + r3, cy + r3), i * 45 - 1.5, i * 45 + 1.5, fill=(255, 255, 255, 230))
    r4 = r * 0.1
    draw.ellipse(S(cx - r4, cy - r4, cx + r4, cy + r4), fill=(255, 255, 255, 255))


def berries(draw, cx, cy, r, color):
    dark = mix(color, (0, 0, 0, 255), 0.35)
    for dx, dy in [(-0.9, 0.3), (0.9, 0.3), (0, -0.5), (0, 0.9)]:
        x, y = cx + dx * r, cy + dy * r
        draw.ellipse(S(x - r, y - r, x + r, y + r), fill=color, outline=dark, width=6 * SS)
        draw.ellipse(S(x - r * 0.45, y - r * 0.55, x - r * 0.1, y - r * 0.2), fill=(255, 255, 255, 140))


def peach(draw, cx, cy, r, color):
    draw.ellipse(S(cx - r, cy - r * 0.95, cx + r, cy + r), fill=color)
    draw.arc(S(cx - r * 0.25, cy - r * 0.9, cx + r * 0.6, cy + r * 0.8), 200, 300, fill=mix(color, (180, 40, 30, 255), 0.5), width=8 * SS)
    draw.ellipse(S(cx + r * 0.1, cy - r * 1.35, cx + r * 0.9, cy - r * 0.85), fill=(80, 170, 70, 255))


def popcorn(draw, cx, cy, s, tint):
    for dx, dy, k in [(-1, 0, 1), (0, -0.7, 1.1), (1, 0, 0.95), (0.1, 0.55, 1), (-0.5, -0.4, 0.8), (0.55, -0.45, 0.85)]:
        x, y, r = cx + dx * s * 0.55, cy + dy * s * 0.55, s * 0.42 * k
        draw.ellipse(S(x - r, y - r, x + r, y + r), fill=tint, outline=mix(tint, (160, 110, 30, 255), 0.4), width=3 * SS)


def bar_illustration(draw, cx, cy, w, h, choc, drizzle):
    draw.rounded_rectangle(S(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h * 0.35 * SS, fill=choc)
    draw.rounded_rectangle(S(cx - w / 2 + 10, cy - h / 2 + 8, cx + w / 2 - 10, cy - h / 2 + 22), radius=7 * SS, fill=mix(choc, (255, 255, 255, 255), 0.25))
    for i in range(7):
        x = cx - w / 2 + 30 + i * (w - 60) / 6
        draw.line(S(x - 22, cy + h / 2 - 12, x + 22, cy - h / 2 + 12), fill=drizzle, width=7 * SS)


# ---------- pack shapes ----------
def can(p):
    img = Image.new("RGBA", (SIZE * SS, SIZE * SS), (0, 0, 0, 0))
    cx, w, top, bottom = 600, 400, 170, 1050
    shadow(img, cx, bottom + 5, 230, 30)
    body_col = hexrgb(p["color"])
    # body
    body = shading(w * SS, (bottom - top) * SS, body_col)
    mask = Image.new("L", body.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 40 * SS, w * SS, (bottom - top) * SS], radius=55 * SS, fill=255)
    md.rectangle([14 * SS, 0, (w - 14) * SS, 120 * SS], fill=255)
    img.paste(body, (int((cx - w / 2) * SS), top * SS), mask)
    d = ImageDraw.Draw(img)
    # lid
    silver = shading((w - 28) * SS, 40 * SS, hexrgb("#C9CCD6"), highlight=0.6)
    lid_mask = Image.new("L", silver.size, 0)
    ImageDraw.Draw(lid_mask).rounded_rectangle([0, 0, *silver.size], radius=16 * SS, fill=255)
    img.paste(silver, (int((cx - w / 2 + 14) * SS), (top - 26) * SS), lid_mask)
    d.ellipse(S(cx - w / 2 + 14, top - 44, cx + w / 2 - 14, top - 8), fill=hexrgb("#E3E5EC"), outline=hexrgb("#9EA2AE"), width=4 * SS)
    # bottom rim
    d.rounded_rectangle(S(cx - w / 2 + 24, bottom - 16, cx + w / 2 - 24, bottom + 6), radius=10 * SS, fill=hexrgb("#B5B9C4"))
    # label band
    ink = hexrgb(p["ink"])
    band_top = top + 330
    d.rectangle(S(cx - w / 2 + 2, band_top, cx + w / 2 - 2, band_top + 230), fill=hexrgb(p["accent"]))
    text_center(d, cx, top + 70, BRAND, "black", 46, ink, w - 80)
    p["art"](d, cx, top + 215, 95)
    y = text_center(d, cx, band_top + 34, p["line1"], "black", 84, ink, w - 70)
    text_center(d, cx, y + 16, p["line2"], "black", 84, ink, w - 70)
    text_center(d, cx, band_top + 268, p["kind"], "bold", 34, (255, 255, 255, 255), w - 90)
    text_center(d, cx, bottom - 120, "12 FL OZ · 0g SUGAR", "bold", 26, (255, 255, 255, 230), w - 100)
    return img


def bag(p):
    img = Image.new("RGBA", (SIZE * SS, SIZE * SS), (0, 0, 0, 0))
    cx, w, top, bottom = 600, 600, 130, 1060
    shadow(img, cx, bottom + 4, 300, 30)
    col = hexrgb(p["color"])
    body = shading(w * SS, (bottom - top) * SS, col, edge_dark=0.35, highlight=0.25, hl_pos=0.3)
    mask = Image.new("L", body.size, 0)
    md = ImageDraw.Draw(mask)
    bh = bottom - top
    # pillow pouch: slightly pinched sides, zigzag crimp top and bottom
    pts = []
    teeth = 16
    for i in range(teeth + 1):
        x = 20 + i * (w - 40) / teeth
        pts.append((x, 0 if i % 2 == 0 else 22))
    pts += [(w - 20, 70), (w, 200), (w - 6, bh - 200), (w - 20, bh - 70)]
    for i in range(teeth, -1, -1):
        x = 20 + i * (w - 40) / teeth
        pts.append((x, bh if i % 2 == 0 else bh - 22))
    pts += [(20, bh - 70), (6, bh - 200), (0, 200), (20, 70)]
    md.polygon([(x * SS, y * SS) for x, y in pts], fill=255)
    img.paste(body, (int((cx - w / 2) * SS), top * SS), mask)
    d = ImageDraw.Draw(img)
    dark = mix(col, (0, 0, 0, 255), 0.25)
    for y in (top + 70, bottom - 70):
        d.line(S(cx - w / 2 + 22, y, cx + w / 2 - 22, y), fill=dark, width=5 * SS)
    ink = hexrgb(p["ink"])
    text_center(d, cx, top + 120, BRAND, "black", 50, ink, w - 160)
    # label oval
    d.ellipse(S(cx - 230, top + 210, cx + 230, top + 600), fill=hexrgb(p["accent"]))
    y = text_center(d, cx, top + 300, p["line1"], "black", 92, ink, 380)
    text_center(d, cx, y + 18, p["line2"], "black", 92, ink, 380)
    text_center(d, cx, top + 528, p["kind"], "bold", 34, ink, 300)
    for x, y, s in [(cx - 150, bottom - 210, 90), (cx + 10, bottom - 175, 100), (cx + 165, bottom - 215, 85), (cx - 60, bottom - 280, 70), (cx + 95, bottom - 300, 70)]:
        popcorn(d, x, y, s, hexrgb(p["kernel"]))
    return img


def box(p):
    img = Image.new("RGBA", (SIZE * SS, SIZE * SS), (0, 0, 0, 0))
    x0, y0, w, h, depth = 300, 180, 540, 860, 80
    shadow(img, x0 + w / 2 + 40, y0 + h + 6, 330, 32)
    d = ImageDraw.Draw(img)
    col, ink = hexrgb(p["color"]), hexrgb(p["ink"])
    # side and top faces
    d.polygon(S(x0 + w, y0, x0 + w + depth, y0 - depth * 0.55, x0 + w + depth, y0 + h - depth * 0.55, x0 + w, y0 + h), fill=mix(col, (0, 0, 0, 255), 0.28))
    d.polygon(S(x0, y0, x0 + depth, y0 - depth * 0.55, x0 + w + depth, y0 - depth * 0.55, x0 + w, y0), fill=mix(col, (255, 255, 255, 255), 0.25))
    # front face with subtle vertical shading
    front = shading(w * SS, h * SS, col, edge_dark=0.12, highlight=0.12, hl_pos=0.2)
    img.paste(front, (x0 * SS, y0 * SS))
    d = ImageDraw.Draw(img)
    cx = x0 + w / 2
    text_center(d, cx, y0 + 60, BRAND, "black", 52, ink, w - 120)
    d.rounded_rectangle(S(x0 + 40, y0 + 150, x0 + w - 40, y0 + 470), radius=36 * SS, fill=hexrgb(p["accent"]))
    y = text_center(d, cx, y0 + 190, p["line1"], "black", 86, ink, w - 120)
    text_center(d, cx, y + 18, p["line2"], "black", 86, ink, w - 120)
    text_center(d, cx, y0 + 410, p["kind"], "bold", 34, ink, w - 140)
    bar_illustration(d, cx, y0 + 600, 400, 110, hexrgb(p["bar"]), hexrgb(p["drizzle"]))
    # protein badge
    bx, by, r = x0 + w - 95, y0 + h - 120, 72
    d.ellipse(S(bx - r, by - r, bx + r, by + r), fill=ink)
    text_center(d, bx, by - 42, "12g", "black", 48, col, 110)
    text_center(d, bx, by + 10, "PROTEIN", "bold", 20, col, 110)
    text_center(d, x0 + 170, y0 + h - 110, "12 BARS", "black", 40, ink, 240)
    return img


def art_citrus(rind, flesh):
    return lambda d, x, y, r: citrus(d, x, y, r, hexrgb(rind), hexrgb(flesh))


PRODUCTS = [
    # Sparkling soda (cans)
    dict(file="grapefruit-sparkling-soda", shape=can, color="#FF6B6B", accent="#FFE15D", ink="#3B0E8C", line1="GRAPE", line2="FRUIT", kind="SPARKLING SODA", art=art_citrus("#FF9F43", "#FF4D6D")),
    dict(file="lime-sparkling-soda", shape=can, color="#2EC27E", accent="#F4FF8A", ink="#0B3D2E", line1="ZESTY", line2="LIME", kind="SPARKLING SODA", art=art_citrus("#1E8C4E", "#B6F36A")),
    dict(file="peach-mango-sparkling-soda", shape=can, color="#FF9F1C", accent="#FFD6E8", ink="#5A1A00", line1="PEACH", line2="MANGO", kind="SPARKLING SODA", art=lambda d, x, y, r: peach(d, x, y, r * 0.85, hexrgb("#FF7B54"))),
    dict(file="wild-berry-sparkling-soda", shape=can, color="#7B2FF7", accent="#7DF9FF", ink="#2A0A5E", line1="WILD", line2="BERRY", kind="SPARKLING SODA", art=lambda d, x, y, r: berries(d, x, y, r * 0.45, hexrgb("#E0457B"))),
    # Popcorn (bags)
    dict(file="sea-salt-popcorn", shape=bag, color="#3DA5FF", accent="#FFFFFF", ink="#0B2A6B", line1="SEA", line2="SALT", kind="POPCORN", kernel="#FFF6D8"),
    dict(file="kettle-corn-popcorn", shape=bag, color="#FFC93C", accent="#FF4F8B", ink="#3B0E8C", line1="KETTLE", line2="CORN", kind="SWEET & SALTY", kernel="#FFE7A3"),
    dict(file="white-cheddar-popcorn", shape=bag, color="#FF6A3D", accent="#FFF3B0", ink="#4A1200", line1="WHITE", line2="CHEDDAR", kind="POPCORN", kernel="#FFE08A"),
    dict(file="chili-lime-popcorn", shape=bag, color="#14B8A6", accent="#FFE15D", ink="#06302B", line1="CHILI", line2="LIME", kind="POPCORN", kernel="#FFEFC0"),
    # Protein bars (boxes)
    dict(file="chocolate-chip-protein-bars", shape=box, color="#FF8FB1", accent="#FFF1F5", ink="#4B1D10", line1="CHOC", line2="CHIP", kind="PROTEIN BARS", bar="#6B3A1E", drizzle="#F6E3C8"),
    dict(file="peanut-butter-protein-bars", shape=box, color="#FFB238", accent="#FFF4D6", ink="#4A2300", line1="PEANUT", line2="BUTTER", kind="PROTEIN BARS", bar="#C98432", drizzle="#5B2E0E"),
    dict(file="birthday-cake-protein-bars", shape=box, color="#8EC5FF", accent="#FFE0F0", ink="#2A1B6B", line1="BIRTHDAY", line2="CAKE", kind="PROTEIN BARS", bar="#F7E6C4", drizzle="#FF5FA2"),
    dict(file="cookies-and-cream-protein-bars", shape=box, color="#2B2D6E", accent="#E9EAFF", ink="#FFFFFF", line1="COOKIES", line2="& CREAM", kind="PROTEIN BARS", bar="#3A2A2A", drizzle="#FFFFFF"),
]

# Fix ink on the dark box: label text sits on a light panel, so use a dark ink there
PRODUCTS[-1]["ink"] = "#2B2D6E"
PRODUCTS[-1]["color"] = "#5A5FD6"

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for p in PRODUCTS:
        img = p["shape"](p).resize((SIZE, SIZE), Image.LANCZOS)
        img.save(OUT / f"{p['file']}.png", optimize=True)
        print("wrote", p["file"])
