```
            ▒█████████▒                                             
           █████████████                                                      
          ███   ███   ███                                                                   
  ████   ████   ███   ████    ▓▓                                                                                  
  ▓██░  ░██ ▒█████████░ ██   ████                                                                                      
░███████░██ ██████████▒ ██   █████   ░▒▓███████▓▒░░▒▓████████▓▒░▒▓████████▓▒░     ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░ 
 ██▒ ▓██████ ▒███████  ███████████▓  ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░           ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
         ██████     ███████▒         ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░           ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
            ███████████▓             ░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
               ▓█████                ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░           ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
          ██████   █████▒            ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░           ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
  ▒███▒█████░         ▓█████▓██▒     ░▒▓███████▓▒░░▒▓████████▓▒░▒▓█▓▒░            ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░
   █████▒                ░█████                                                              
    ████                   ███                                                                                    
     ██                    ██                                                   
 _ ____|_________________________________________ ____  /\_____ ______________________________________________|____ _ _
       |                                              \/              STICKERWALL IDENTIFIER & INDEXER v0.23  |
```

![Python](https://img.shields.io/badge/python%2B-blue)
![Type](https://img.shields.io/badge/type-CLI-informational)
![Security](https://img.shields.io/badge/hacking-hackallthethings)

## Dear Hackers,

Have you or a loved one every wished you had a way to identify all the @defcon #stickerwall stickers?
If you have, this repo does all the  work. 

* https://defcon.hakc.ai --> https://github.com/haKC-ai/defcon_stickerwall_id
* https://stickerwall.hakc.ai --> https://docs.google.com/spreadsheets/d/1fEpmuktaH_FUu2C8xge5xQNcIpusEovC9kNNXWdyfTE/edit?gid=0#gid=0

  * Public Google Sheet output for the DEF CON 33 stickerwall

<p align="center">
  <img src="https://raw.githubusercontent.com/haKC-ai/defcon_stickerwall_id/main/res/images/DCSIDTv23.png" alt="STICKERWALL IDENTIFIER & INDEXER v0.23" width="1600"/>
</p>

`What this script does` 

It slices a large sticker wall image into overlapping tiles, identify all stickers per tile with OpenAI Vision, and streams the results to CSV in real time.



```
NAME........................................StickerWall Auto-ID  
Collective...........................[haKC.ai / COP DETECTED]  
System..................Python3 / OpenAI Vision / LocalIO  
Size..........................................[IN PROGRESS...]  
Supplied by......................................./dev/CØR.23  
Release date...........................................2025  

GROUP NEWS: Bigger tiles, smarter cuts, faster IDs.  
            No cloud slop, just raw wall hacker magic.  

NFO:  
* Overlapping tile crops ensure full sticker capture  
* Multi-object detection per tile via model-guided parse  
* CSV streamed live for tail’n as results land  
* Defanged websites for safe share’n  
* Local-first, security-minded design (minimal deps)  

OUTPUT:  
  stickers_out/tiles/*.jpg..................tile crops  
  stickers_out/stickers.csv.................raw tiles  
  stickers_out/stickers_identified.csv......multi results streamed  
  stickers_out/contact_sheet.jpg............visual index  
  stickers_out/auto_id.log..................run log  

PIPELINE:  
  [Input wall.jpg] -> Slice tiles -> Filter (brightness/edges)  
  -> Save JPGs -> Call OpenAI Vision -> Parse JSON  
  -> Defang URLs -> Stream CSV -> QA loop  

CSV SCHEMA:  
  thumbnail | x | y | tile_w | tile_h | mean_brightness | edge_mean  
  name | category | notes | confidence | website | model | tile_index  

TUNING:  
  * --tile-w / --tile-h up = bigger crops  
  * --stride-x / --stride-y down = more overlap  
  * --min-brightness / --min-edge-mean down = keep more tiles  
  * --max-tiles cap = recon mode  


GR33TZ: SecKC, DEF CON, LEGACY CoWTownComputerCongress, ACiD,  
        iCE, T$A, badge lords  

SHOUTZ:  
[*] Stickerheads grinding walls at 2AM  
[*] Sysops still riding 14.4k jammers  
[*] AOHELL punter fiends with dusty ANSIs  

FU to [LAMERZ] dropping full URLs in pastebins.  

───── ▓ signed, /dev/CØR.23: ▓ ─────  
"im stuck on you"  
```

## Quick start

```bash
# 1. Create and activate a virtualenv, then install deps
python3 -m venv .venv_stickers
source .venv_stickers/bin/activate
pip install -r requirements.txt

# 2. Configure OpenAI
export OPENAI_API_KEY="sk-..."; export OPENAI_VISION_MODEL="gpt-4o-mini"

# 3. Run
python sticker_id_auto.py \
  --input wall.jpg \
  --outdir stickers_out \
  --tile-w 300 --tile-h 300 \
  --stride-x 200 --stride-y 200 \
  --min-brightness 8 \
  --min-edge-mean 2 \
  --format jpg \
  --contact-sheet \
  --rate-limit 1.0
```

Outputs

* `stickers_out/tiles/*.jpg`
* `stickers_out/stickers.csv` raw tiles
* `stickers_out/stickers_identified.csv` multi row results streamed as processed
* `stickers_out/auto_id.log` run log
* `stickers_out/contact_sheet.jpg` optional visual index

## Mermaid pipeline

```mermaid
flowchart TD
    A[Input stickerwall.jpg] --> B[Slice into overlapping tiles]
    B -->|Filter by brightness and edges| C[Save tile images]
    C --> D[For each tile call OpenAI Vision]
    D -->|Prompt requests array of stickers| E[Parse JSON array]
    E -->|Defang URLs and sanitize| F[Stream append to stickers_identified.csv]
    F --> G[Continuous review and QA]
    C --> H[Generate contact_sheet.jpg]
```

## CSV schema

`stickers_identified.csv` fields

* `thumbnail` file name of the tile image
* `x` `y` top left pixel coordinate in the original wall
* `tile_w` `tile_h` tile dimensions
* `mean_brightness` `edge_mean` filter metrics
* `name` model reported name per detected sticker
* `category` freeform category such as conference or tool
* `notes` short notes or raw fallback text
* `confidence` 0 to 1 if provided
* `website` defanged, example hxxps\://defcon\[.]org
* `model` vision model used
* `tile_index` index of the item within the tile if multiple

## Tuning

* Increase `--tile-w` and `--tile-h` for bigger crops
* Reduce `--stride-x` and `--stride-y` to increase overlap and reduce cutoff risk
* Lower `--min-brightness` and `--min-edge-mean` to keep more tiles
* `--max-tiles` can cap processing for a fast reconnaissance pass

## Prompt strategy

The default prompt asks for an array of objects with fields
`name, category, confidence, notes, website`.
The parser accepts either an array or single object. It also removes code fences.
If parsing fails, the script falls back to a single row that preserves raw text in `notes`.

## Security model

* No network calls beyond the OpenAI API
* Local slicing and file IO only
* URLs are defanged before writing to CSV
* Logs stored locally under `stickers_out/auto_id.log`
* Environment variables via `python-dotenv` supported if you prefer a `.env` file

## Example monitoring

```bash
tail -f stickers_out/auto_id.log
tail -f stickers_out/stickers_identified.csv
```

## Minimal requirements

See `requirements.txt`

```
pillow
numpy
python-dotenv
openai
tenacity
```

## Troubleshooting

* `OPENAI_API_KEY missing`
  Set `export OPENAI_API_KEY="sk-..."` or use a `.env` file.

* CSV rows look like one sticker per tile
  Verify you are running the multi result script and did not override `--prompt`.

* Too many cut stickers
  Increase tile size and reduce stride. Example 384 by 384 tiles with 160 stride.

* False positives or noisy results
  Add a post filter that drops items with `confidence < 0.4`, or add a second pass that merges duplicates by `name` and keeps the highest confidence.

