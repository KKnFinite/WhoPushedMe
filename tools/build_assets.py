from pathlib import Path
from PIL import Image, ImageOps
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]

ASSETS_SRC = ROOT / "static" / "assets_src"
ASSETS = ROOT / "static" / "assets"
STATIC_ICONS = ROOT / "static" / "icons"
META = ASSETS / "_meta"

OFFICIAL_ICON = ASSETS_SRC / "icons" / "WPM_DesktopIcon_Official.jpg"
TRANSPARENT_MASCOT = ASSETS_SRC / "mascots" / "master" / "WPM_Mascot_FullBody_Transparent.png"
ONBOARDING_MASCOTS_SRC = ASSETS_SRC / "mascots" / "onboarding"
ONBOARDING_MASCOTS = ASSETS / "mascots" / "onboarding"
HOME_BACKGROUNDS_SRC = ASSETS_SRC / "home" / "backgrounds"
HOME_BACKGROUNDS = ASSETS / "home" / "backgrounds"
HOME_BACKGROUND_SOURCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
HOME_HEROES_SRC = ASSETS_SRC / "home" / "heroes"
HOME_HEROES = ASSETS / "home" / "heroes"

EVENT_MAP = {
    ("joining", "new-player"): "player_join_new",
    ("joining", "returning-player"): "player_join_returning",
    ("joining", "spectator"): "player_join_spectator",
    ("round", "start"): "round_start",
    ("score", "push"): "score_push",
    ("round-end", "winner"): "round_end_winner",
    ("round-end", "head-to-head-loser"): "round_end_head_to_head_loser",
    ("round-end", "not-last"): "round_end_not_last",
    ("round-end", "dead-last"): "round_end_dead_last",
    ("round-end", "complete"): "round_end_complete",
}


def ensure_parent(path):
    path.parent.mkdir(parents=True, exist_ok=True)


def image_info(path):
    with Image.open(path) as im:
        bands = im.getbands()
        alpha = None
        if "A" in bands:
            alpha = list(im.getchannel("A").getextrema())
        return {
            "dimensions": [im.width, im.height],
            "mode": im.mode,
            "real_alpha": bool(alpha and alpha[0] < 255),
            "alpha_extrema": alpha,
        }


def make_webp(src, dst, *, lossless=True):
    ensure_parent(dst)

    with Image.open(src) as im:
        if "A" in im.getbands():
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")

        if lossless:
            im.save(dst, "WEBP", lossless=True, method=6)
        else:
            im.save(dst, "WEBP", quality=92, method=6)

    print("WEBP:", dst.relative_to(ROOT))


def make_square_icon(src, dst, size):
    ensure_parent(dst)

    with Image.open(src) as im:
        im = im.convert("RGB")

        square = ImageOps.fit(
            im,
            (size, size),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

        square.save(dst, "PNG", optimize=True)

    print("ICON:", dst.relative_to(ROOT), f"{size}x{size}")


def validate_sources():
    required = [
        ASSETS_SRC / "brand" / "WPM_Wordmark.png",
        ASSETS_SRC / "brand" / "WPM_SecondaryBadge.png",
        ASSETS_SRC / "mascots" / "master" / "WPM_Mascot_FullBody.png",
        TRANSPARENT_MASCOT,
        OFFICIAL_ICON,
    ]

    missing = [p for p in required if not p.exists()]

    if missing:
        raise SystemExit(
            "Missing required masters:\n" +
            "\n".join(str(p.relative_to(ROOT)) for p in missing)
        )

    mini_pngs = sorted(
        (ASSETS_SRC / "mascots" / "mini").rglob("*.png")
    )

    mini_webps = sorted(
        (ASSETS / "mascots" / "mini").rglob("*.webp")
    )

    print("Mini PNG masters:", len(mini_pngs))
    print("Mini WebPs:", len(mini_webps))

    if len(mini_pngs) != len(mini_webps):
        raise SystemExit(
            "Mini PNG/WebP counts do not match. Stopping before cleanup."
        )

    # Verify every master has a production counterpart.
    missing_webp = []

    for png in mini_pngs:
        rel = png.relative_to(ASSETS_SRC)
        expected = (ASSETS / rel).with_suffix(".webp")

        if not expected.exists():
            missing_webp.append(expected)

    if missing_webp:
        raise SystemExit(
            "Missing mini production WebPs:\n" +
            "\n".join(str(p.relative_to(ROOT)) for p in missing_webp)
        )

    hero_pngs = sorted(HOME_HEROES_SRC.glob("*.png")) if HOME_HEROES_SRC.exists() else []
    hero_webps = sorted(HOME_HEROES.glob("*.webp")) if HOME_HEROES.exists() else []
    print("Home hero PNG masters:", len(hero_pngs))
    print("Home hero WebPs:", len(hero_webps))
    if len(hero_pngs) != len(hero_webps):
        raise SystemExit(
            "Home hero PNG/WebP counts do not match. Stopping before cleanup."
        )

    missing_hero_webp = [
        HOME_HEROES / f"{png.stem}.webp"
        for png in hero_pngs
        if not (HOME_HEROES / f"{png.stem}.webp").exists()
    ]
    if missing_hero_webp:
        raise SystemExit(
            "Missing Home hero production WebPs:\n" +
            "\n".join(str(p.relative_to(ROOT)) for p in missing_hero_webp)
        )


def build_home_background_webps():
    if not HOME_BACKGROUNDS_SRC.exists():
        return

    for source in sorted(HOME_BACKGROUNDS_SRC.iterdir()):
        if not source.is_file():
            continue
        if source.suffix.lower() not in HOME_BACKGROUND_SOURCE_EXTENSIONS:
            continue

        production = HOME_BACKGROUNDS / f"{source.stem}.webp"
        if source.suffix.lower() == ".webp":
            ensure_parent(production)
            shutil.copy2(source, production)
            print("WEBP:", production.relative_to(ROOT), "(copied exact source)")
        else:
            make_webp(source, production, lossless=False)


def build_home_hero_webps():
    if not HOME_HEROES_SRC.exists():
        return

    for source in sorted(HOME_HEROES_SRC.glob("*.png")):
        production = HOME_HEROES / f"{source.stem}.webp"
        make_webp(source, production, lossless=False)


def build_core_webps():
    make_webp(
        ASSETS_SRC / "brand" / "WPM_Wordmark.png",
        ASSETS / "brand" / "WPM_Wordmark.webp",
        lossless=True,
    )

    make_webp(
        ASSETS_SRC / "brand" / "WPM_SecondaryBadge.png",
        ASSETS / "brand" / "WPM_SecondaryBadge.webp",
        lossless=True,
    )

    make_webp(
        ASSETS_SRC / "mascots" / "master" / "WPM_Mascot_FullBody.png",
        ASSETS / "mascots" / "master" / "WPM_Mascot_FullBody.webp",
        lossless=True,
    )

    make_webp(
        TRANSPARENT_MASCOT,
        ASSETS / "mascots" / "master" / "WPM_Mascot_FullBody_Transparent.webp",
        lossless=True,
    )

    make_webp(
        OFFICIAL_ICON,
        ASSETS / "icons" / "WPM_DesktopIcon_Official.webp",
        lossless=False,
    )

    alt_src = ASSETS_SRC / "icons" / "alternates"
    alt_out = ASSETS / "icons" / "alternates"

    if alt_src.exists():
        for src in sorted(alt_src.iterdir()):
            if not src.is_file():
                continue

            if src.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue

            make_webp(
                src,
                alt_out / f"{src.stem}.webp",
                lossless=src.suffix.lower() == ".png",
            )


def build_onboarding_webps():
    if not ONBOARDING_MASCOTS_SRC.exists():
        return

    for src in sorted(ONBOARDING_MASCOTS_SRC.rglob("*.png")):
        rel = src.relative_to(ONBOARDING_MASCOTS_SRC)
        make_webp(
            src,
            (ONBOARDING_MASCOTS / rel).with_suffix(".webp"),
            lossless=False,
        )


def build_pwa_icons():
    STATIC_ICONS.mkdir(parents=True, exist_ok=True)

    make_square_icon(
        OFFICIAL_ICON,
        STATIC_ICONS / "icon-32.png",
        32,
    )

    make_square_icon(
        OFFICIAL_ICON,
        STATIC_ICONS / "apple-touch-icon-180.png",
        180,
    )

    make_square_icon(
        OFFICIAL_ICON,
        STATIC_ICONS / "icon-192.png",
        192,
    )

    make_square_icon(
        OFFICIAL_ICON,
        STATIC_ICONS / "icon-512.png",
        512,
    )


def archive_old_loose_minis():
    old_dir = ASSETS / "mascots" / "mini"
    archive = ASSETS_SRC / "mascots" / "legacy-mini"

    if not old_dir.exists():
        return

    loose = sorted(old_dir.glob("WPM_Mini_*.png"))

    if not loose:
        return

    archive.mkdir(parents=True, exist_ok=True)

    for src in loose:
        dst = archive / src.name

        if not dst.exists():
            shutil.copy2(src, dst)

        src.unlink()
        print("ARCHIVED:", dst.relative_to(ROOT))


def update_web_manifest():
    path = ROOT / "static" / "manifest.webmanifest"

    data = json.loads(path.read_text(encoding="utf-8"))

    data["icons"] = [
        {
            "src": "/static/icons/icon-192.png",
            "sizes": "192x192",
            "type": "image/png",
            "purpose": "any",
        },
        {
            "src": "/static/icons/icon-512.png",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any",
        },
    ]

    path.write_text(
        json.dumps(data, indent=2) + "\n",
        encoding="utf-8",
    )

    print("UPDATED:", path.relative_to(ROOT))


def update_home():
    path = ROOT / "templates" / "home.html"
    text = path.read_text(encoding="utf-8")

    old_favicon = (
        """  <link rel="icon" type="image/svg+xml" """
        """href="{{ url_for('static', filename='icon.svg') }}">"""
    )

    new_favicon = (
        """  <link rel="icon" type="image/png" sizes="32x32" """
        """href="{{ url_for('static', filename='icons/icon-32.png') }}">\n"""
        """  <link rel="apple-touch-icon" sizes="180x180" """
        """href="{{ url_for('static', filename='icons/apple-touch-icon-180.png') }}">"""
    )

    if old_favicon in text:
        text = text.replace(old_favicon, new_favicon)
    elif new_favicon not in text:
        raise SystemExit("Neither expected old nor current favicon markup found.")

    text = text.replace(
        """{{ url_for('static', filename='icon.svg') }}""",
        """{{ url_for('static', filename='assets/icons/WPM_DesktopIcon_Official.webp') }}""",
    )

    path.write_text(text, encoding="utf-8")
    print("UPDATED:", path.relative_to(ROOT))


def update_service_worker():
    path = ROOT / "static" / "service-worker.js"

    content = """const CACHE_NAME = 'wpm-shell-v53';

const APP_SHELL = [
  '/',
  '/static/app.css',
  '/static/app.js',
  '/static/manifest.webmanifest',
  '/static/assets/_meta/asset-manifest.json',
  '/static/icons/icon-32.png',
  '/static/icons/apple-touch-icon-180.png',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/assets/icons/WPM_DesktopIcon_Official.webp',
  '/static/assets/brand/WPM_Splash_Login.webp',
  '/static/assets/brand/WPM_Wordmark.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_BrightDay.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_CreekBridge.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_GoldenHour.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_StormySunset.webp',
  '/static/assets/home/heroes/WPM_Home_Hero_SunriseCourse.webp'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );

  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const requestUrl = new URL(event.request.url);

  if (requestUrl.origin !== self.location.origin) return;

  // Never cache live/shared round API data.
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Navigation stays network-first with an offline shell fallback.
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();

          caches.open(CACHE_NAME).then((cache) => {
            cache.put('/', copy);
          });

          return response;
        })
        .catch(() => caches.match('/'))
    );

    return;
  }

  // Static assets are cache-first.
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;

      return fetch(event.request).then((response) => {
        if (response.ok) {
          const copy = response.clone();

          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, copy);
          });
        }

        return response;
      });
    })
  );
});
"""

    path.write_text(content, encoding="utf-8")
    print("UPDATED:", path.relative_to(ROOT))


def update_requirements():
    path = ROOT / "requirements.txt"

    lines = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not any(line.lower().startswith("pillow") for line in lines):
        lines.append("Pillow>=12,<13")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("UPDATED:", path.relative_to(ROOT))


def infer_mini_metadata(src):
    rel = src.relative_to(
        ASSETS_SRC / "mascots" / "mini"
    )

    parts = rel.parts

    category = parts[0] if len(parts) >= 1 else None
    situation = parts[1] if len(parts) >= 2 else None

    event_key = EVENT_MAP.get((category, situation))

    prod_rel = (
        Path("mascots")
        / "mini"
        / rel
    ).with_suffix(".webp")

    production = ASSETS / prod_rel

    return category, situation, event_key, production


def build_manifest():
    META.mkdir(parents=True, exist_ok=True)

    entries = []

    core = [
        (
            "brand.wordmark",
            ASSETS_SRC / "brand" / "WPM_Wordmark.png",
            ASSETS / "brand" / "WPM_Wordmark.webp",
            "brand",
        ),
        (
            "brand.secondary_badge",
            ASSETS_SRC / "brand" / "WPM_SecondaryBadge.png",
            ASSETS / "brand" / "WPM_SecondaryBadge.webp",
            "brand",
        ),
        (
            "mascot.full_body",
            ASSETS_SRC / "mascots" / "master" / "WPM_Mascot_FullBody.png",
            ASSETS / "mascots" / "master" / "WPM_Mascot_FullBody.webp",
            "mascot-master",
        ),
        (
            "mascot.full_body.transparent",
            TRANSPARENT_MASCOT,
            ASSETS / "mascots" / "master" / "WPM_Mascot_FullBody_Transparent.webp",
            "mascot-master",
        ),
        (
            "icon.official",
            OFFICIAL_ICON,
            ASSETS / "icons" / "WPM_DesktopIcon_Official.webp",
            "icon",
        ),
    ]

    for asset_id, source, production, family in core:
        entries.append(
            {
                "asset_id": asset_id,
                "family": family,
                "source": source.relative_to(ROOT).as_posix(),
                "production": production.relative_to(ROOT).as_posix(),
                **image_info(source),
            }
        )

    alt_src = ASSETS_SRC / "icons" / "alternates"

    if alt_src.exists():
        for source in sorted(alt_src.iterdir()):
            if not source.is_file():
                continue

            if source.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
                continue

            production = (
                ASSETS
                / "icons"
                / "alternates"
                / f"{source.stem}.webp"
            )

            entries.append(
                {
                    "asset_id": f"icon.alternate.{source.stem}",
                    "family": "icon-alternate",
                    "source": source.relative_to(ROOT).as_posix(),
                    "production": production.relative_to(ROOT).as_posix(),
                    **image_info(source),
                }
            )

    onboarding_root = ONBOARDING_MASCOTS_SRC

    onboarding_count = 0

    if onboarding_root.exists():
        for source in sorted(onboarding_root.rglob("*.png")):
            rel = source.relative_to(onboarding_root)
            production = (ONBOARDING_MASCOTS / rel).with_suffix(".webp")

            if not production.exists():
                raise SystemExit(
                    f"Missing onboarding production pair for {source.relative_to(ROOT)}"
                )

            onboarding_count += 1

            situation = rel.parts[0] if len(rel.parts) >= 2 else "general"

            entries.append(
                {
                    "asset_id": (
                        "onboarding."
                        + rel.with_suffix("")
                        .as_posix()
                        .replace("/", ".")
                    ),
                    "family": "onboarding-mascot",
                    "category": "onboarding",
                    "situation": situation,
                    "source": source.relative_to(ROOT).as_posix(),
                    "production": production.relative_to(ROOT).as_posix(),
                    **image_info(source),
                }
            )

    home_background_count = 0

    if HOME_BACKGROUNDS_SRC.exists():
        for source in sorted(HOME_BACKGROUNDS_SRC.iterdir()):
            if not source.is_file():
                continue
            if source.suffix.lower() not in HOME_BACKGROUND_SOURCE_EXTENSIONS:
                continue

            production = HOME_BACKGROUNDS / f"{source.stem}.webp"
            if not production.exists():
                raise SystemExit(
                    f"Missing Home background production pair for {source.relative_to(ROOT)}"
                )

            home_background_count += 1
            short_name = source.stem
            prefix = "WPM_Home_Background_"
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix):]

            entries.append(
                {
                    "asset_id": f"home.background.{short_name}",
                    "family": "home-background",
                    "pool": "home.backgrounds",
                    "enabled": True,
                    "source": source.relative_to(ROOT).as_posix(),
                    "production": production.relative_to(ROOT).as_posix(),
                    **image_info(source),
                }
            )

    home_hero_count = 0

    if HOME_HEROES_SRC.exists():
        for source in sorted(HOME_HEROES_SRC.glob("*.png")):
            production = HOME_HEROES / f"{source.stem}.webp"
            if not production.exists():
                raise SystemExit(
                    f"Missing Home hero production pair for {source.relative_to(ROOT)}"
                )

            home_hero_count += 1
            short_name = source.stem
            prefix = "WPM_Home_Hero_"
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix):]

            entries.append(
                {
                    "asset_id": f"home.hero.{short_name}",
                    "family": "home-hero",
                    "pool": "home.heroes",
                    "enabled": True,
                    "source": source.relative_to(ROOT).as_posix(),
                    "production": production.relative_to(ROOT).as_posix(),
                    **image_info(source),
                }
            )

    mini_root = ASSETS_SRC / "mascots" / "mini"

    mini_count = 0

    if mini_root.exists():
        for source in sorted(mini_root.rglob("*.png")):
            category, situation, event_key, production = infer_mini_metadata(source)

            if not production.exists():
                raise SystemExit(
                    f"Missing production pair for {source.relative_to(ROOT)}"
                )

            mini_count += 1

            entries.append(
                {
                    "asset_id": (
                        "mini."
                        + source.relative_to(mini_root)
                        .with_suffix("")
                        .as_posix()
                        .replace("/", ".")
                    ),
                    "family": "mini-mascot",
                    "category": category,
                    "situation": situation,
                    "event_key": event_key,
                    "source": source.relative_to(ROOT).as_posix(),
                    "production": production.relative_to(ROOT).as_posix(),
                    **image_info(source),
                }
            )

    manifest = {
        "schema_version": 1,
        "official_icon_source": (
            "static/assets_src/icons/WPM_DesktopIcon_Official.jpg"
        ),
        "mini_asset_count": mini_count,
        "onboarding_asset_count": onboarding_count,
        "home_background_count": home_background_count,
        "home_hero_count": home_hero_count,
        "assets": entries,
    }

    manifest_path = META / "asset-manifest.json"

    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = META / "ASSET_README.txt"

    readme.write_text(
        """WHO PUSHED ME?! ASSET FOUNDATION

MASTER / SOURCE ART
static/assets_src/

PRODUCTION WEB ART
static/assets/

PWA / DEVICE ICONS
static/icons/

OFFICIAL APP ICON SOURCE
static/assets_src/icons/WPM_DesktopIcon_Official.jpg

CORE RULES
- PNG/JPG mascot and brand masters remain untouched in assets_src.
- Home background source art may be PNG, JPG, JPEG, or WebP; production copies are WebP.
- Home hero masters live under assets_src/home/heroes as PNG; production copies are WebP.
- Web UI should prefer production WebP assets.
- PWA/device icons remain PNG.
- WPM_DesktopIcon_Official.jpg is the official app icon source.
- WPM_Mascot_FullBody.png is the original approved full-body mascot; golf bag is allowed.
- WPM_Mascot_FullBody_Transparent.png is the transparent full-body app/compositing master.
- Mini mascots use their categorized event folders.
- Onboarding mascots live under mascots/onboarding and are UI assets, not gameplay minis.
- Do not replace approved art with rejected generations.
""",
        encoding="utf-8",
    )

    print("MANIFEST:", manifest_path.relative_to(ROOT))
    print("Mini assets in manifest:", mini_count)
    print("Home backgrounds in manifest:", home_background_count)
    print("Home heroes in manifest:", home_hero_count)


def cleanup_duplicates():
    old_files = [
        ASSETS / "brand" / "WPM_Wordmark.png",
        ASSETS / "brand" / "WPM_SecondaryBadge.png",
        ASSETS / "mascots" / "WPM_Mascot_FullBody.png",
        ASSETS / "icons" / "WPM_AppIcon_1024.png",
        ASSETS / "icons" / "WPM_DesktopIcon_Official.jpg",
    ]

    old_alt_dir = ASSETS / "icons" / "alternates"

    if old_alt_dir.exists():
        old_files.extend(
            p
            for p in old_alt_dir.iterdir()
            if p.is_file()
            and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
        )

    for path in old_files:
        if path.exists():
            path.unlink()
            print("REMOVED DUPLICATE:", path.relative_to(ROOT))

    for root_file in [
        ROOT / "asset-manifest.json",
        ROOT / "ASSET_README.txt",
    ]:
        if root_file.exists():
            root_file.unlink()
            print("REMOVED OLD ROOT METADATA:", root_file.name)

    old_svg = ROOT / "static" / "icon.svg"

    if old_svg.exists():
        old_svg.unlink()
        print("REMOVED:", old_svg.relative_to(ROOT))


def main():
    validate_sources()
    build_core_webps()
    build_home_background_webps()
    build_home_hero_webps()
    build_onboarding_webps()
    build_pwa_icons()
    archive_old_loose_minis()

    update_web_manifest()
    update_home()
    update_service_worker()
    update_requirements()

    cleanup_duplicates()
    build_manifest()

    mini_pngs = list(
        (ASSETS_SRC / "mascots" / "mini").rglob("*.png")
    )

    mini_webps = list(
        (ASSETS / "mascots" / "mini").rglob("*.webp")
    )

    print()
    print("================================")
    print("ASSET FOUNDATION COMPLETE")
    print("================================")
    print("Mini PNG masters:", len(mini_pngs))
    print("Mini WebPs:", len(mini_webps))
    print(
        "Onboarding mascot masters:",
        len(list(ONBOARDING_MASCOTS_SRC.rglob("*.png")))
        if ONBOARDING_MASCOTS_SRC.exists()
        else 0,
    )
    print("Official icon:", OFFICIAL_ICON.relative_to(ROOT))
    print("Old icon.svg exists:", (ROOT / "static/icon.svg").exists())


if __name__ == "__main__":
    main()
