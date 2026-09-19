from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PIL import Image

from tools.build_assets import ASSETS, ASSETS_SRC, build_manifest, make_webp
from who_pushed_me.content.catalog import CONTENT_DIR, ContentCatalog, ContentError, EventRegistry
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


def cmd_validate(args: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate(strict_mascot_audit=args.strict_audit)
    summary = catalog.mascot_audit_summary()
    print("Content library valid.")
    print(f"Events: {len(catalog.registry.events)}")
    print(f"Triggerable events: {sum(bool(e.get('triggerable')) for e in catalog.registry.events.values())}")
    print(f"Themes: {len(catalog.themes)}")
    print(f"Banter messages: {len(catalog.banter)}")
    print(f"Mini mascot metadata rows: {len(catalog.mascots)}")
    print(f"Mini audit verified: {summary.get('verified', 0)}")
    print(f"Mini audit pending: {summary.get('pending', 0)}")


def cmd_list_events(_: argparse.Namespace) -> None:
    registry = EventRegistry.load()
    for row in registry.selectable_events(include_scopes=True):
        marker = "event" if row.get("triggerable") else "scope"
        print(f"{row['key']:<48} {marker:<5} {row['label']}")


def _open_image(path: Path) -> None:
    try:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
    except OSError as error:
        print(f"Could not open image automatically: {error}")


def _prompt_keep(label: str, current: str | None = None, *, required: bool = False) -> str:
    suffix = f" [{current}]" if current else ""
    while True:
        value = input(f"{label}{suffix}: ").strip()
        if value:
            return value
        if current:
            return current
        if not required:
            return ""
        print("A value is required.")


def _prompt_choice(label: str, current: str, choices: list[str]) -> str:
    rendered = " / ".join(choices)
    while True:
        value = input(f"{label} [{current}] ({rendered}): ").strip().lower()
        if not value:
            return current
        if value in choices:
            return value
        print(f"Choose one of: {rendered}")


def _prompt_themes(catalog: ContentCatalog, current: list[str]) -> list[str]:
    available = sorted(catalog.themes)
    shown = ", ".join(current) if current else "none"
    print(f"Themes currently: {shown}")
    print("Available themes: " + (", ".join(available) if available else "none"))
    raw = input("Themes comma-separated, ENTER to keep: ").strip()
    if not raw:
        return current
    if raw.lower() in {"none", "-"}:
        return []
    values = [value.strip() for value in raw.split(",") if value.strip()]
    unknown = [value for value in values if value not in catalog.themes]
    if unknown:
        raise ContentError(f"unknown content themes: {unknown}")
    return list(dict.fromkeys(values))


def _prompt_signs(copy: str, current: list[str]) -> list[str]:
    shown = " | ".join(current) if current else copy
    raw = input(f"Sign panels, separate with | [{shown}]: ").strip()
    if not raw:
        return current or [copy]
    return [value.strip() for value in raw.split("|") if value.strip()]


def _manifest_mini_map(catalog: ContentCatalog) -> dict[str, dict]:
    return {
        row["asset_id"]: row
        for row in catalog.asset_manifest.get("assets", [])
        if row.get("family") == "mini-mascot"
    }


def _copy_hint(asset: dict, family: str, registry: EventRegistry) -> str:
    stem = Path(str(asset["source"])).stem
    prefix = str(
        registry.asset_families.get(family, {}).get("prefix") or ""
    )
    if prefix and stem.startswith(prefix):
        stem = stem[len(prefix):]
    stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
    stem = re.sub(r"(?<=[A-Za-z])(?=[0-9])|(?<=[0-9])(?=[A-Za-z])", " ", stem)
    return " ".join(stem.split())


def cmd_audit_status(_: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()
    summary = catalog.mascot_audit_summary()
    print(f"Verified: {summary.get('verified', 0)}")
    print(f"Pending:  {summary.get('pending', 0)}")

    manifest = _manifest_mini_map(catalog)
    groups: dict[str, dict[str, int]] = {}
    for row in catalog.mascots:
        asset = manifest.get(row["asset_id"], {})
        family = "/".join(
            part
            for part in [asset.get("category"), asset.get("situation")]
            if part
        ) or "unknown"
        bucket = groups.setdefault(family, {"verified": 0, "pending": 0})
        status = row.get("audit_status", "pending")
        bucket[status] = bucket.get(status, 0) + 1

    print()
    for family in sorted(groups):
        bucket = groups[family]
        print(
            f"{family:<34} "
            f"verified={bucket.get('verified', 0):>2} "
            f"pending={bucket.get('pending', 0):>2}"
        )


def cmd_audit_minis(args: argparse.Namespace) -> None:
    path = CONTENT_DIR / "mascots.json"
    data = _read(path)
    rows = list(data.get("mascots") or [])
    catalog = ContentCatalog.load()
    catalog.validate()
    manifest = _manifest_mini_map(catalog)

    selected = []
    for row in rows:
        asset = manifest.get(row["asset_id"])
        if not asset:
            continue
        family = "/".join(
            part
            for part in [asset.get("category"), asset.get("situation")]
            if part
        )
        if args.family and family != args.family:
            continue
        if args.asset_id and row["asset_id"] != args.asset_id:
            continue
        if not args.all and row.get("audit_status") == "verified":
            continue
        selected.append((row, asset, family))

    if not selected:
        print("No mascot assets match the audit filter.")
        return

    print(f"Mascots queued for audit: {len(selected)}")
    print("Commands at confirmation: v=verify/save, s=skip, q=quit")
    print()

    for index, (row, asset, family) in enumerate(selected, start=1):
        png = ROOT / asset["source"]
        print("=" * 72)
        print(f"[{index}/{len(selected)}] {row['asset_id']}")
        print(f"Family: {family}")
        print(f"PNG: {asset['source']}")
        print(f"Current events: {', '.join(row.get('events') or [])}")
        print(f"Current vulgarity: {row.get('vulgarity', 'normal')}")
        print(
            "Current themes: "
            + (", ".join(row.get("themes") or []) or "none")
        )
        print()

        if not args.no_open:
            _open_image(png)

        suggested_copy = row.get("copy") or _copy_hint(
            asset,
            family,
            catalog.registry,
        )
        print(f"Filename-derived copy hint: {suggested_copy}")
        copy = _prompt_keep(
            "Exact visible sign/message copy",
            suggested_copy,
            required=True,
        )
        signs = _prompt_signs(copy, list(row.get("signs") or []))
        hat_copy = _prompt_keep("Hat copy (optional)", row.get("hat_copy")) or None

        events = list(row.get("events") or [])
        edit_events = input(
            "Eligible events/scopes: ENTER keeps current, E edits: "
        ).strip().lower()
        if edit_events == "e":
            events = _choose_events(catalog.registry)

        vulgarity = _prompt_choice(
            "Vulgarity",
            str(row.get("vulgarity") or "normal"),
            ["normal", "brutal"],
        )
        themes = _prompt_themes(catalog, list(row.get("themes") or []))
        notes = _prompt_keep("Notes (optional)", row.get("notes"))

        action = input("Verify/save this mascot? [v/s/q]: ").strip().lower()
        if action == "q":
            print("Audit stopped. Previous verified items were already saved.")
            return
        if action != "v":
            print("Skipped.")
            continue

        row.update(
            {
                "copy": copy,
                "signs": signs,
                "hat_copy": hat_copy,
                "events": events,
                "vulgarity": vulgarity,
                "themes": themes,
                "notes": notes,
                "audit_status": "verified",
            }
        )
        data["mascots"] = rows
        _write(path, data)
        ContentCatalog.load().validate()
        print("Verified and saved.")
        print()

    print("Audit queue complete.")



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

    copy = args.copy or input("Exact visible sign/message copy: ").strip()
    if not copy:
        raise ContentError("mini copy is required")
    signs = list(args.sign or []) or [copy]
    hat_copy = args.hat_copy or None

    rows.append(
        {
            "asset_id": asset_id,
            "copy": copy,
            "signs": signs,
            "hat_copy": hat_copy,
            "events": events,
            "vulgarity": args.vulgarity,
            "themes": themes,
            "enabled": True,
            "notes": args.notes or "",
            "audit_status": "verified",
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
    validate.add_argument(
        "--strict-audit",
        action="store_true",
        help="fail unless every existing mini has been visually audited",
    )
    validate.set_defaults(func=cmd_validate)

    audit_status = subparsers.add_parser(
        "audit-status",
        help="show verified/pending mascot metadata counts",
    )
    audit_status.set_defaults(func=cmd_audit_status)

    audit_minis = subparsers.add_parser(
        "audit-minis",
        help="visually audit existing mascot metadata one image at a time",
    )
    audit_minis.add_argument(
        "--family",
        help="limit to category/situation, e.g. round-end/complete",
    )
    audit_minis.add_argument("--asset-id", help="audit one exact mascot asset_id")
    audit_minis.add_argument(
        "--all",
        action="store_true",
        help="include already verified mascot records",
    )
    audit_minis.add_argument(
        "--no-open",
        action="store_true",
        help="do not open the PNG in the default image viewer",
    )
    audit_minis.set_defaults(func=cmd_audit_minis)

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
    add_mini.add_argument("--copy")
    add_mini.add_argument(
        "--sign",
        action="append",
        help="visible sign panel copy; repeat for multiple panels",
    )
    add_mini.add_argument("--hat-copy")
    add_mini.add_argument("--notes")
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
