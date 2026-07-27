from __future__ import annotations

import csv
import time
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

ITEMS = [
    ("Aloraichium Z", "aloraichiumz"),
    ("Buginium Z", "buginiumz"),
    ("Darkinium Z", "darkiniumz"),
    ("Decidium Z", "decidiumz"),
    ("Dragonium Z", "dragoniumz"),
    ("Eevium Z", "eeviumz"),
    ("Electrium Z", "electriumz"),
    ("Fairium Z", "fairiumz"),
    ("Fightinium Z", "fightiniumz"),
    ("Firium Z", "firiumz"),
    ("Flyinium Z", "flyiniumz"),
    ("Ghostium Z", "ghostiumz"),
    ("Grassium Z", "grassiumz"),
    ("Groundium Z", "groundiumz"),
    ("Icium Z", "iciumz"),
    ("Incinium Z", "inciniumz"),
    ("Kommonium Z", "kommoniumz"),
    ("Lunalium Z", "lunaliumz"),
    ("Lycanium Z", "lycaniumz"),
    ("Marshadium Z", "marshadiumz"),
    ("Mewnium Z", "mewniumz"),
    ("Mimikium Z", "mimikiumz"),
    ("Normalium Z", "normaliumz"),
    ("Pikanium Z", "pikaniumz"),
    ("Pikashunium Z", "pikashuniumz"),
    ("Poisonium Z", "poisoniumz"),
    ("Primarium Z", "primariumz"),
    ("Psychium Z", "psychiumz"),
    ("Rockium Z", "rockiumz"),
    ("Snorlium Z", "snorliumz"),
    ("Solganium Z", "solganiumz"),
    ("Steelium Z", "steeliumz"),
    ("Tapunium Z", "tapuniumz"),
    ("Ultranecrozium Z", "ultranecroziumz"),
    ("Waterium Z", "wateriumz"),
]

ROOT = Path("Z-Crystals")
STANDARD = ROOT / "Standard"
LARGE = ROOT / "Large PGL"
ZIP_PATH = Path("Z-Crystals.zip")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/150 Safari/537.36"


def download(url: str, destination: Path, retries: int = 3) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        print(f"Exists: {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Referer": "https://www.serebii.net/"})
    last_error: Exception | None = None

    for attempt in range(1, retries + 1):
        try:
            with urlopen(request, timeout=30) as response:
                data = response.read()
                content_type = response.headers.get("Content-Type", "")
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                    raise RuntimeError(f"Response was not a PNG ({content_type}, {len(data)} bytes)")
                destination.write_bytes(data)
                print(f"Downloaded: {destination}")
                return
        except Exception as exc:
            last_error = exc
            print(f"Attempt {attempt}/{retries} failed for {url}: {exc}")
            time.sleep(attempt * 1.5)

    raise RuntimeError(f"Unable to download {url}") from last_error


def main() -> None:
    STANDARD.mkdir(parents=True, exist_ok=True)
    LARGE.mkdir(parents=True, exist_ok=True)

    with (ROOT / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["name", "slug", "standard_url", "large_pgl_url"])
        for name, slug in ITEMS:
            standard_url = f"https://www.serebii.net/itemdex/sprites/{slug}.png"
            large_url = f"https://www.serebii.net/itemdex/sprites/pgl/{slug}.png"
            writer.writerow([name, slug, standard_url, large_url])

            download(standard_url, STANDARD / f"{name}.png")
            time.sleep(0.2)
            download(large_url, LARGE / f"{name}.png")
            time.sleep(0.2)

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.as_posix())

    print(f"\nComplete: {ZIP_PATH.resolve()}")
    print(f"Included {len(ITEMS)} standard sprites and {len(ITEMS)} large PGL sprites.")


if __name__ == "__main__":
    main()
