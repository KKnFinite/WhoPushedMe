from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from PIL import Image

from tools.build_assets import ASSETS, ASSETS_SRC, build_manifest, make_webp
from who_pushed_me.content.catalog import CONTENT_DIR, ContentCatalog, ContentError, EventRegistry

ROOT = Path(__file__).resolve().parents[1]
MINI_SRC = ASSETS_SRC / "mascots" / "mini"
MINI_PROD = ASSETS / "mascots" / "mini"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _pascal_slug(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    if not words:
        raise ContentError("short name must contain letters or numbers")
    return "".join(word[:1].upper() + word[1:] for word in words)


def _choose_events(registry: EventRegistry) -> list[str]:
    rows = registry.selectable_events(include_scopes=True)
    print("\nSELECT ELIGIBLE EVENTS / SCOPES")
    for index, row in enumerate(rows, start=1):
        marker = "EVENT" if row.get("triggerable") else "SCOPE"
        print(f"{index:>3}. [{marker}] {row['key']} - {row['label']}")
    raw = input("\nNumbers or event keys, comma-separated: ").strip()
    if not raw:
        raise ContentError("at least one event is required")

    selected: list[str] = []
    by_key = {row["key"] for row in rows}
    for token in [part.strip() for part in raw.split(",") if part.strip()]:
        if token.isdigit():
            index = int(token)
            if index < 1 or index > len(rows):
                raise ContentError(f"event selection out of range: {token}")
            key = rows[index - 1]["key"]
        else:
            key = registry.canonical_key(token)
            if key not in by_key:
                raise ContentError(f"event cannot be selected for content: {token}")
        if key not in selected:
            selected.append(key)
    return selected


def _events_from_args(registry: EventRegistry, values: list[str] | None) -> list[str]:
    if not values:
        return _choose_events(registry)
    result = []
    for value in values:
        key = registry.canonical_key(value)
        if key not in result:
            result.append(key)
    return result


def _themes_from_args(catalog: ContentCatalog, values: list[str] | None) -> list[str]:
    result = []
    for value in values or []:
        if value not in catalog.themes:
            raise ContentError(f"unknown content theme: {value}")
        if value not in result:
            result.append(value)
    return result


def cmd_validate(_: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()
    print("Content library valid.")
    print(f"Events: {len(catalog.registry.events)}")
    print(f"Triggerable events: {sum(bool(e.get('triggerable')) for e in catalog.registry.events.values())}")
    print(f"Themes: {len(catalog.themes)}")
    print(f"Banter messages: {len(catalog.banter)}")
    print(f"Mini mascot metadata rows: {len(catalog.mascots)}")


def cmd_list_events(_: argparse.Namespace) -> None:
    registry = EventRegistry.load()
    for row in registry.selectable_events(include_scopes=True):
        marker = "event" if row.get("triggerable") else "scope"
        print(f"{row['key']:<48} {marker:<5} {row['label']}")


def cmd_add_banter(args: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()
    events = _events_from_args(catalog.registry, args.event)
    themes = _themes_from_args(catalog, args.theme)
    text = args.text or input("Banter text: ").strip()
    if not text:
        raise ContentError("banter text cannot be empty")

    slug = _pascal_slug(args.short_name or " ".join(text.split()[:7]))
    content_id = f"banter.{slug}"
    path = CONTENT_DIR / "banter.json"
    data = _read(path)
    rows = list(data.get("banter") or [])
    if any(row.get("id") == content_id for row in rows):
        raise ContentError(f"banter id already exists: {content_id}")

    rows.append(
        {
            "id": content_id,
            "text": text,
            "events": events,
            "audiences": [args.audience],
            "vulgarity": args.vulgarity,
            "themes": themes,
            "enabled": True,
        }
    )
    data["banter"] = sorted(rows, key=lambda row: row["id"])
    _write(path, data)
    ContentCatalog.load().validate()
    print(f"Added {content_id}")


def cmd_add_mini(args: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()
    registry = catalog.registry
    source = Path(args.png).expanduser().resolve()
    if not source.exists():
        raise ContentError(f"PNG not found: {source}")
    if source.suffix.lower() != ".png":
        raise ContentError("mini source must be a PNG")

    with Image.open(source) as image:
        if "A" not in image.getbands():
            raise ContentError("mini PNG has no alpha channel")
        if image.getchannel("A").getextrema()[0] == 255:
            raise ContentError("mini PNG has no real transparency")

    events = _events_from_args(registry, args.event)
    themes = _themes_from_args(catalog, args.theme)

    derived_families = {
        family
        for event_key in events
        if (family := registry.asset_family(event_key))
    }
    family = args.family
    if family is None:
        if len(derived_families) == 1:
            family = next(iter(derived_families))
        else:
            print("\nAvailable asset families:")
            for key in sorted(registry.asset_families):
                print(f"  {key}")
            family = input("Storage family: ").strip()

    if family not in registry.asset_families:
        raise ContentError(f"unknown asset family: {family}")

    short_name = _pascal_slug(args.short_name or source.stem)
    prefix = registry.asset_families[family]["prefix"]
    stem = prefix + short_name
    relative_dir = Path(*family.split("/"))
    destination_png = MINI_SRC / relative_dir / f"{stem}.png"
    destination_webp = MINI_PROD / relative_dir / f"{stem}.webp"

    if destination_png.exists() or destination_webp.exists():
        raise ContentError(f"asset already exists: {stem}")

    destination_png.parent.mkdir(parents=True, exist_ok=True)
    destination_webp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination_png)
    make_webp(destination_png, destination_webp, lossless=True)

    rel = destination_png.relative_to(MINI_SRC)
    asset_id = (
        "mini."
        + rel.with_suffix("").as_posix().replace("/", ".")
    )

    metadata_path = CONTENT_DIR / "mascots.json"
    metadata = _read(metadata_path)
    rows = list(metadata.get("mascots") or [])
    if any(row.get("asset_id") == asset_id for row in rows):
        raise ContentError(f"mascot metadata already exists: {asset_id}")

    rows.append(
        {
            "asset_id": asset_id,
            "events": events,
            "vulgarity": args.vulgarity,
            "themes": themes,
            "enabled": True,
        }
    )
    metadata["mascots"] = sorted(rows, key=lambda row: row["asset_id"])
    _write(metadata_path, metadata)

    build_manifest()
    ContentCatalog.load().validate()

    print(f"Added mini: {asset_id}")
    print(f"PNG: {destination_png.relative_to(ROOT)}")
    print(f"WebP: {destination_webp.relative_to(ROOT)}")
    print("Asset manifest and content metadata validated.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WHO PUSHED ME?! content administration")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate all event/content metadata")
    validate.set_defaults(func=cmd_validate)

    list_events = subparsers.add_parser("list-events", help="list content events and scopes")
    list_events.set_defaults(func=cmd_list_events)

    add_banter = subparsers.add_parser("add-banter", help="add a banter message")
    add_banter.add_argument("--text")
    add_banter.add_argument("--short-name")
    add_banter.add_argument("--event", action="append")
    add_banter.add_argument("--theme", action="append")
    add_banter.add_argument("--vulgarity", choices=["normal", "brutal"], default="normal")
    add_banter.add_argument(
        "--audience",
        choices=["everyone", "actor", "target", "subject", "others", "team"],
        default="everyone",
    )
    add_banter.set_defaults(func=cmd_add_banter)

    add_mini = subparsers.add_parser("add-mini", help="import a transparent mini PNG")
    add_mini.add_argument("png")
    add_mini.add_argument("--short-name")
    add_mini.add_argument("--event", action="append")
    add_mini.add_argument("--theme", action="append")
    add_mini.add_argument("--family")
    add_mini.add_argument("--vulgarity", choices=["normal", "brutal"], default="normal")
    add_mini.set_defaults(func=cmd_add_mini)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except ContentError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
