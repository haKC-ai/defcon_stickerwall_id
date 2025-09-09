#!/usr/bin/env python3
import os, sys, csv, argparse, logging, base64, time, json, re
from pathlib import Path
import numpy as np
from PIL import Image, ImageStat, ImageFilter, ImageDraw, ImageFont
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI
import fade

try:
    from banner import print_banner_side_by_side
    HAVE_BANNER = True
except Exception:
    HAVE_BANNER = False

BASE_FIELDS = ["thumbnail","x","y","tile_w","tile_h","mean_brightness","edge_mean"]
AI_FIELDS   = ["name","category","notes","confidence","website","model","tile_index"]

def parse_args():
    p = argparse.ArgumentParser(description="Slice a wall image, identify stickers, and produce CSV + map with grid overlay.")
    p.add_argument("--input", required=True)
    p.add_argument("--outdir", default="stickers_out")
    p.add_argument("--tile-w", type=int, default=300)
    p.add_argument("--tile-h", type=int, default=300)
    p.add_argument("--stride-x", type=int, default=200)
    p.add_argument("--stride-y", type=int, default=200)
    p.add_argument("--min-brightness", type=float, default=8.0)
    p.add_argument("--min-edge-mean", type=float, default=2.0)
    p.add_argument("--max-tiles", type=int, default=0)
    p.add_argument("--format", choices=["jpg","png"], default="jpg")
    p.add_argument("--quality", type=int, default=95)
    p.add_argument("--raw-csv", default="stickers.csv")
    p.add_argument("--out-csv", default="stickers_identified.csv")
    p.add_argument("--contact-sheet", action="store_true")
    p.add_argument("--model", default=os.environ.get("OPENAI_VISION_MODEL","gpt-4o-mini"))
    p.add_argument("--rate-limit", type=float, default=1.0)
    p.add_argument("--prompt", default=(
        "Identify all distinct stickers or logos in this image. "
        "Return a JSON array. Each element must be an object with keys: "
        "name, category, confidence (0 to 1), notes, website. "
        "Use official site when known. Keep notes concise."
    ))
    p.add_argument("--thumbnail-base-url", default="", help="Base raw URL for tiles. Example: https://raw.githubusercontent.com/.../tiles")
    p.add_argument("--image-mode", type=int, default=4)
    p.add_argument("--image-width", type=int, default=100)
    p.add_argument("--image-height", type=int, default=100)
    return p.parse_args()

def ensure_dir(p: Path): p.mkdir(parents=True, exist_ok=True)
def gray(img): return img.convert("L")
def mean_brightness(img): return ImageStat.Stat(gray(img)).mean[0]
def edge_mean(img): return float(np.asarray(gray(img).filter(ImageFilter.FIND_EDGES)).mean())

def slice_image(src_path, outdir, tile_w, tile_h, sx, sy, min_brightness, min_edge_mean, max_tiles, quality, fmt, csv_name, build_contact_sheet):
    img = Image.open(src_path).convert("RGB")
    W, H = img.size
    tiles_dir = outdir / "tiles"; ensure_dir(tiles_dir)
    csv_path = outdir / csv_name
    rows, saved = [], 0
    for y in range(0, H - tile_h + 1, sy):
        for x in range(0, W - tile_w + 1, sx):
            tile = img.crop((x, y, x + tile_w, y + tile_h))
            mb, em = mean_brightness(tile), edge_mean(tile)
            if mb < min_brightness or em < min_edge_mean: continue
            name = f"{x}_{y}.{fmt}"
            params = {"quality": quality} if fmt == "jpg" else {}
            tile.save(tiles_dir / name, **params)
            rows.append({"thumbnail": name, "x": x, "y": y, "tile_w": tile_w, "tile_h": tile_h,
                         "mean_brightness": round(mb,3), "edge_mean": round(em,3)})
            saved += 1
            if max_tiles and saved >= max_tiles: break
        if max_tiles and saved >= max_tiles: break
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=BASE_FIELDS); writer.writeheader(); writer.writerows(rows)

    if build_contact_sheet and rows:
        import math
        thumb_w = thumb_h = 120
        cols = int(math.sqrt(min(len(rows), 400))) or 1
        rows_ct = (len(rows) + cols - 1) // cols
        sheet = Image.new("RGB", (cols*thumb_w, rows_ct*thumb_h), (24,24,24))
        for idx, r in enumerate(rows[:cols*rows_ct]):
            timg = Image.open(tiles_dir / r["thumbnail"]).convert("RGB").resize((thumb_w, thumb_h), Image.LANCZOS)
            cx = (idx % cols) * thumb_w
            cy = (idx // cols) * thumb_h
            sheet.paste(timg, (cx, cy))
        sheet.save(outdir / "contact_sheet.jpg", quality=90)

    map_img = img.copy()
    draw = ImageDraw.Draw(map_img)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    for r in rows:
        x, y, tw, th = r["x"], r["y"], r["tile_w"], r["tile_h"]
        draw.rectangle([x, y, x+tw, y+th], outline="red", width=2)
        coord_label = f"{x},{y}"
        draw.text((x+5, y+5), coord_label, fill="yellow", font=font)

    map_img.save(outdir / "map_with_grid.jpg", quality=90)
    return csv_path

def defang_url(url: str) -> str:
    if not url: return ""
    return url.replace("http://","hxxp://").replace("https://","hxxps://").replace(".","[.]")

def strip_code_fence(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z0-9]*\s*", "", s)
        s = re.sub(r"\s*```$", "", s)
    return s.strip()

def parse_multi_json(txt: str):
    t = strip_code_fence(txt)
    try:
        data = json.loads(t)
    except Exception:
        m = re.search(r"\[.*\]|\{.*\}", t, flags=re.S)
        if not m: return []
        try:
            data = json.loads(m.group(0))
        except Exception:
            return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []
    cleaned = []
    for item in data:
        if not isinstance(item, dict): continue
        cleaned.append({
            "name": str(item.get("name","")).strip(),
            "category": str(item.get("category","")).strip(),
            "notes": str(item.get("notes","")).strip(),
            "confidence": item.get("confidence",""),
            "website": defang_url(str(item.get("website","")).strip())
        })
    return cleaned

def b64_image(p: Path) -> str: return base64.b64encode(open(p,"rb").read()).decode("ascii")

def init_openai():
    load_dotenv()
    key = os.environ.get("OPENAI_API_KEY")
    if not key: raise RuntimeError("OPENAI_API_KEY missing. Add it to .env")
    return OpenAI(api_key=key)

@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=30), reraise=True)
def identify_all_in_tile(client, model, img_path, prompt):
    content = [
        {"type":"text","text":prompt},
        {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64_image(img_path)}"}}
    ]
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role":"user","content":content}],
        temperature=0.1
    )
    txt = (resp.choices[0].message.content or "").strip()
    items = parse_multi_json(txt)
    if not items:
        items = [{"name": txt[:120], "category": "", "notes": "freeform", "confidence": "", "website": ""}]
    return items

def join_url(base: str, name: str) -> str:
    if not base: return name
    return base.rstrip("/") + "/" + name.lstrip("/")

def image_formula(url: str, mode: int, w: int, h: int) -> str:
    return f'=IMAGE("{url}", {mode}, {w}, {h})'

def main():
    if HAVE_BANNER:
        try: print_banner_side_by_side()
        except: pass
    BANNER_TEXT = """
    _ ____|____________________________________________ ____  /\_____ __________________________________________________|____ _ _
          |                                                 \/                  STICKERWALL IDENTIFIER & INDEXER v0.23  |
""" 
    print(fade.brazil(BANNER_TEXT))

    args = parse_args()
    outdir = Path(args.outdir); ensure_dir(outdir)
    tiles_dir = outdir / "tiles"; ensure_dir(tiles_dir)

    log_path = outdir / "auto_id.log"
    logging.basicConfig(filename=str(log_path), level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    raw_csv = slice_image(Path(args.input), outdir, args.tile_w, args.tile_h, args.stride_x, args.stride_y,
                          args.min_brightness, args.min_edge_mean, args.max_tiles, args.quality, args.format,
                          args.raw_csv, args.contact_sheet)

    client = init_openai()
    model = args.model
    delay = 1.0 / max(args.rate_limit, 0.001)

    out_csv = outdir / args.out_csv
    fieldnames = BASE_FIELDS + AI_FIELDS
    if not out_csv.exists():
        with open(out_csv, "w", newline="") as f:
            csv.DictWriter(f, fieldnames=fieldnames).writeheader()

    rows = list(csv.DictReader(open(raw_csv)))
    total = len(rows)
    for i, r in enumerate(rows, 1):
        img_path = tiles_dir / r["thumbnail"]
        try:
            results = identify_all_in_tile(client, model, img_path, args.prompt)
        except Exception as e:
            results = [{"name": "", "category": "", "notes": f"error:{e}", "confidence": "", "website": ""}]

        raw_url = join_url(args.thumbnail_base_url, r["thumbnail"]) if args.thumbnail_base_url else r["thumbnail"]
        thumb_formula = image_formula(raw_url, args.image_mode, args.image_width, args.image_height)

        with open(out_csv, "a", newline="") as f_out:
            w = csv.DictWriter(f_out, fieldnames=fieldnames)
            for j, item in enumerate(results):
                out_row = dict(r)
                out_row["thumbnail"] = thumb_formula
                out_row.update({
                    "name": item.get("name",""),
                    "category": item.get("category",""),
                    "notes": item.get("notes",""),
                    "confidence": item.get("confidence",""),
                    "website": item.get("website",""),
                    "model": model,
                    "tile_index": j
                })
                w.writerow(out_row)

        print(f"[{i}/{total}] {r['thumbnail']} -> {len(results)} item(s)")
        logging.info("[%d/%d] %s -> %d", i, total, r["thumbnail"], len(results))
        time.sleep(delay)

    print(f"Wrote {out_csv}")

if __name__ == "__main__":
    main()
