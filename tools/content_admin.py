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
from who_pushed_me.store import RoundStore
MINI_SRC = ASSETS_SRC / "mascots" / "mini"
MINI_PROD = ASSETS / "mascots" / "mini"
HOME_BACKGROUND_SRC = ASSETS_SRC / "home" / "backgrounds"
HOME_BACKGROUND_PROD = ASSETS / "home" / "backgrounds"
HOME_BACKGROUND_SOURCE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _pascal_slug(value: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", value)
    if not words:
        raise ContentError("short name must contain letters or numbers")
    return "".join(word[:1].upper() + word[1:] for word in words)


def _choose_events(
    registry: EventRegistry,
    current: list[str] | None = None,
) -> list[str]:
    rows = registry.selectable_events(include_scopes=True)
    print("\nSELECT ELIGIBLE EVENTS")
    for index, row in enumerate(rows, start=1):
        print(f"{index:>3}. {row['label']}")
    if current:
        current_labels = [
            registry.event(event_key)["label"]
            for event_key in current
        ]
        print("Current: " + ", ".join(current_labels))
        raw = input(
            "\nNumbers, comma-separated; ENTER keeps current: "
        ).strip()
        if not raw:
            return list(current)
    else:
        raw = input("\nNumbers, comma-separated: ").strip()
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


def cmd_runtime_status(_: argparse.Namespace) -> None:
    controls = RoundStore().get_content_runtime_controls()
    print(
        "Mini mascots: "
        + ("ON" if controls["mini_mascots_enabled"] else "OFF")
    )
    print(
        "Trash talk: "
        + ("ON" if controls["trash_talk_enabled"] else "OFF")
    )
    overrides = controls.get("event_overrides") or {}
    print(f"Event overrides: {len(overrides)}")
    for key, enabled in sorted(overrides.items()):
        print(f"  {key}: {'ON' if enabled else 'OFF'}")


def cmd_set_master(args: argparse.Namespace) -> None:
    enabled = args.state == "on"
    kwargs = (
        {"mini_mascots_enabled": enabled}
        if args.kind == "minis"
        else {"trash_talk_enabled": enabled}
    )
    controls = RoundStore().set_content_runtime_master(**kwargs)
    print(
        f"{args.kind}: "
        + (
            "ON"
            if (
                controls["mini_mascots_enabled"]
                if args.kind == "minis"
                else controls["trash_talk_enabled"]
            )
            else "OFF"
        )
    )


def cmd_set_event(args: argparse.Namespace) -> None:
    enabled = {
        "on": True,
        "off": False,
        "default": None,
    }[args.state]
    controls = RoundStore().set_content_event_override(args.event_key, enabled)
    overrides = controls.get("event_overrides") or {}
    if args.state == "default":
        print(f"{args.event_key}: DEFAULT")
    else:
        key = EventRegistry.load().canonical_key(args.event_key)
        print(f"{key}: {'ON' if overrides.get(key) else 'OFF'}")


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
    shortcuts = {
        choice[0].lower(): choice
        for choice in choices
        if sum(1 for other in choices if other.startswith(choice[0])) == 1
    }
    rendered = " | ".join(
        f"{choice[0].upper()} {choice}" if choice[0].lower() in shortcuts else choice
        for choice in choices
    )
    while True:
        value = input(f"{label} [{current}]: ENTER keep | {rendered}: ").strip().lower()
        if not value:
            return current
        if value in choices:
            return value
        if value in shortcuts:
            return shortcuts[value]
        print(f"Choose one of: {rendered}")


def _prompt_themes(catalog: ContentCatalog, current: list[str]) -> list[str]:
    available = sorted(catalog.themes)
    shown = ", ".join(current) if current else "none"

    raw = input(
        f"Themes [{shown}]: ENTER keep | D drinking | W wife | "
        "B both | N none | E edit all: "
    ).strip().lower()

    if not raw:
        return current
    if raw == "n":
        return []
    if raw == "d":
        if "drinking" not in catalog.themes:
            raise ContentError("drinking theme is not registered")
        return ["drinking"]
    if raw == "w":
        if "wife" not in catalog.themes:
            raise ContentError("wife theme is not registered")
        return ["wife"]
    if raw == "b":
        missing = [
            theme for theme in ("drinking", "wife")
            if theme not in catalog.themes
        ]
        if missing:
            raise ContentError(f"themes are not registered: {missing}")
        return ["drinking", "wife"]
    if raw != "e":
        print("Use D, W, B, N, E, or press ENTER.")
        return _prompt_themes(catalog, current)

    print("Available themes: " + (", ".join(available) if available else "none"))
    raw = input("Themes comma-separated: ").strip()
    if not raw or raw.lower() in {"none", "-"}:
        return []

    values = [value.strip() for value in raw.split(",") if value.strip()]
    unknown = [value for value in values if value not in catalog.themes]
    if unknown:
        raise ContentError(f"unknown content themes: {unknown}")
    return list(dict.fromkeys(values))


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


def _suspicious_copy(value: object) -> bool:
    text = str(value or "").strip()
    return len(text) <= 1


def cmd_repair_copy(args: argparse.Namespace) -> None:
    path = CONTENT_DIR / "mascots.json"
    data = _read(path)
    rows = list(data.get("mascots") or [])
    catalog = ContentCatalog.load()
    manifest = _manifest_mini_map(catalog)

    selected = []
    for row in rows:
        if not args.asset_id and not _suspicious_copy(row.get("copy")):
            continue
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
        selected.append((row, asset, family))

    if not selected:
        print("No suspicious mascot copy values found.")
        return

    print(f"Suspicious copy values queued: {len(selected)}")
    print("This only repairs the visible-message copy.")
    print("Hat copy, events, vulgarity, themes, notes, and audit status are preserved.")
    print()

    for index, (row, asset, family) in enumerate(selected, start=1):
        png = ROOT / asset["source"]
        hint = _copy_hint(asset, family, catalog.registry)

        print("=" * 72)
        print(f"[{index}/{len(selected)}] {row['asset_id']}")
        print(f"Current bad copy: {row.get('copy')!r}")
        print(f"Filename-derived hint: {hint}")

        if not args.no_open:
            _open_image(png)

        copy = _prompt_keep(
            "Exact visible sign/message copy",
            hint,
            required=True,
        )
        row["copy"] = copy
        data["mascots"] = rows
        _write(path, data)
        print("Copy repaired and saved.")
        print()

    ContentCatalog.load().validate(strict_mascot_audit=True)
    print("Suspicious-copy repair complete.")


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
        current_event_labels = [
            catalog.registry.event(event_key)["label"]
            for event_key in row.get("events") or []
        ]
        print(
            "Current events: "
            + (", ".join(current_event_labels) or "none")
        )
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
        hat_copy = _prompt_keep("Hat copy (optional)", row.get("hat_copy")) or None

        events = list(row.get("events") or [])
        current_event_labels = [
            catalog.registry.event(event_key)["label"]
            for event_key in events
        ]
        current_events = ", ".join(current_event_labels) if events else "none"
        edit_events = input(
            f"Eligible events [{current_events}]: ENTER keeps current, E edits: "
        ).strip().lower()
        if edit_events == "e":
            events = _choose_events(catalog.registry, current=events)

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



def cmd_list_banter(args: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()

    rows = list(catalog.banter)
    if args.event:
        event_key = catalog.registry.canonical_key(args.event)
        rows = [
            row
            for row in rows
            if event_key in {
                catalog.registry.canonical_key(value)
                for value in row.get("events") or []
            }
        ]
    if args.contains:
        needle = args.contains.lower()
        rows = [
            row
            for row in rows
            if needle in str(row.get("text") or "").lower()
        ]

    for row in rows:
        state = "ON" if row.get("enabled", True) else "OFF"
        print(f"{row['id']:<42} {state:<3} {row['text']}")
    print(f"Messages: {len(rows)}")


def cmd_remove_banter(args: argparse.Namespace) -> None:
    path = CONTENT_DIR / "banter.json"
    data = _read(path)
    rows = list(data.get("banter") or [])
    target = next(
        (row for row in rows if row.get("id") == args.content_id),
        None,
    )
    if target is None:
        raise ContentError(f"banter id not found: {args.content_id}")

    if not args.yes:
        print(f"ID:   {target['id']}")
        print(f"Text: {target['text']}")
        answer = input("Type REMOVE to confirm: ").strip()
        if answer != "REMOVE":
            print("Cancelled.")
            return

    data["banter"] = [
        row for row in rows if row.get("id") != args.content_id
    ]
    _write(path, data)
    ContentCatalog.load().validate()
    print(f"Removed {args.content_id}")


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
    hat_copy = args.hat_copy or None

    rows.append(
        {
            "asset_id": asset_id,
            "copy": copy,
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


def cmd_remove_mini(args: argparse.Namespace) -> None:
    catalog = ContentCatalog.load()
    catalog.validate()

    asset = next(
        (
            row
            for row in catalog.asset_manifest.get("assets", [])
            if row.get("asset_id") == args.asset_id
        ),
        None,
    )
    if asset is None or asset.get("family") != "mini-mascot":
        raise ContentError(f"unknown mini asset_id: {args.asset_id}")

    metadata_path = CONTENT_DIR / "mascots.json"
    metadata = _read(metadata_path)
    rows = list(metadata.get("mascots") or [])
    if not any(row.get("asset_id") == args.asset_id for row in rows):
        raise ContentError(f"mascot metadata not found: {args.asset_id}")

    if not args.yes:
        answer = input(
            f"Remove {args.asset_id} from active assets and content metadata? "
            "Type REMOVE to confirm: "
        ).strip()
        if answer != "REMOVE":
            print("Cancelled.")
            return

    source = ROOT / asset["source"]
    production = ROOT / asset["production"]

    for path in (source, production):
        if path.exists():
            path.unlink()
            print(f"Removed: {path.relative_to(ROOT)}")

    metadata["mascots"] = [
        row for row in rows if row.get("asset_id") != args.asset_id
    ]
    _write(metadata_path, metadata)

    build_manifest()
    ContentCatalog.load().validate()

    print(f"Removed mini: {args.asset_id}")
    print("Asset manifest and content metadata validated.")



def _home_background_sources() -> list[Path]:
    if not HOME_BACKGROUND_SRC.exists():
        return []
    return sorted(
        path
        for path in HOME_BACKGROUND_SRC.iterdir()
        if path.is_file()
        and path.suffix.lower() in HOME_BACKGROUND_SOURCE_EXTENSIONS
    )


def cmd_list_home_backgrounds(_: argparse.Namespace) -> None:
    rows = _home_background_sources()
    for source in rows:
        production = HOME_BACKGROUND_PROD / f"{source.stem}.webp"
        state = "READY" if production.exists() else "MISSING WEBP"
        print(f"{source.stem:<52} {state}")
    print(f"Home backgrounds: {len(rows)}")


def cmd_add_home_background(args: argparse.Namespace) -> None:
    source = Path(args.image).expanduser().resolve()
    if not source.exists():
        raise ContentError(f"background image not found: {source}")
    if source.suffix.lower() not in HOME_BACKGROUND_SOURCE_EXTENSIONS:
        raise ContentError(
            "Home background source must be PNG, JPG, JPEG, or WebP"
        )

    raw_name = args.short_name or source.stem
    prefix = "WPM_Home_Background_"
    if raw_name.startswith(prefix):
        raw_name = raw_name[len(prefix):]
    stem = prefix + _pascal_slug(raw_name)

    existing_sources = [
        path
        for path in _home_background_sources()
        if path.stem == stem
    ]
    destination_webp = HOME_BACKGROUND_PROD / f"{stem}.webp"
    if existing_sources or destination_webp.exists():
        raise ContentError(f"Home background already exists: {stem}")

    destination_source = HOME_BACKGROUND_SRC / f"{stem}{source.suffix.lower()}"
    destination_source.parent.mkdir(parents=True, exist_ok=True)
    destination_webp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination_source)
    make_webp(destination_source, destination_webp, lossless=False)
    build_manifest()

    print(f"Added Home background: {stem}")
    print(f"Source: {destination_source.relative_to(ROOT)}")
    print(f"WebP:   {destination_webp.relative_to(ROOT)}")
    print("Registered in pool: home.backgrounds")


def cmd_remove_home_background(args: argparse.Namespace) -> None:
    token = args.name.strip()
    prefix = "WPM_Home_Background_"
    if token.startswith("home.background."):
        token = token[len("home.background."):]
    if token.startswith(prefix):
        stem = token
    else:
        stem = prefix + _pascal_slug(token)

    matches = [
        path
        for path in _home_background_sources()
        if path.stem == stem
    ]
    production = HOME_BACKGROUND_PROD / f"{stem}.webp"

    if not matches and not production.exists():
        raise ContentError(f"Home background not found: {stem}")

    if not args.yes:
        answer = input(
            f"Remove {stem} from the Home background pool? Type REMOVE to confirm: "
        ).strip()
        if answer != "REMOVE":
            print("Cancelled.")
            return

    for path in [*matches, production]:
        if path.exists():
            path.unlink()
            print(f"Removed: {path.relative_to(ROOT)}")

    build_manifest()
    print(f"Removed Home background: {stem}")


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

    repair_copy = subparsers.add_parser(
        "repair-copy",
        help="repair suspicious one-character mascot message copy values",
    )
    repair_copy.add_argument(
        "--family",
        help="limit to category/situation, e.g. joining/new-player",
    )
    repair_copy.add_argument(
        "--asset-id",
        help="repair one exact mascot asset_id, including a non-suspicious wrong value",
    )
    repair_copy.add_argument(
        "--no-open",
        action="store_true",
        help="do not open the PNG in the default image viewer",
    )
    repair_copy.set_defaults(func=cmd_repair_copy)

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

    runtime_status = subparsers.add_parser(
        "runtime-status",
        help="show Neon-backed master content toggles and event overrides",
    )
    runtime_status.set_defaults(func=cmd_runtime_status)

    set_master = subparsers.add_parser(
        "set-master",
        help="turn all mini mascots or all trash talk on/off",
    )
    set_master.add_argument("kind", choices=["minis", "banter"])
    set_master.add_argument("state", choices=["on", "off"])
    set_master.set_defaults(func=cmd_set_master)

    set_event = subparsers.add_parser(
        "set-event",
        help="set or clear a runtime event/family override",
    )
    set_event.add_argument("event_key")
    set_event.add_argument("state", choices=["on", "off", "default"])
    set_event.set_defaults(func=cmd_set_event)

    list_banter = subparsers.add_parser(
        "list-banter",
        help="list banter messages, optionally filtered by event or text",
    )
    list_banter.add_argument("--event")
    list_banter.add_argument("--contains")
    list_banter.set_defaults(func=cmd_list_banter)

    remove_banter = subparsers.add_parser(
        "remove-banter",
        help="remove one banter message by content id",
    )
    remove_banter.add_argument("content_id")
    remove_banter.add_argument(
        "--yes",
        action="store_true",
        help="remove without interactive confirmation",
    )
    remove_banter.set_defaults(func=cmd_remove_banter)

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

    list_home_backgrounds = subparsers.add_parser(
        "list-home-backgrounds",
        help="list images in the rotating Home background pool",
    )
    list_home_backgrounds.set_defaults(func=cmd_list_home_backgrounds)

    add_home_background = subparsers.add_parser(
        "add-home-background",
        help="import an image into the rotating Home background pool",
    )
    add_home_background.add_argument("image")
    add_home_background.add_argument("--short-name")
    add_home_background.set_defaults(func=cmd_add_home_background)

    remove_home_background = subparsers.add_parser(
        "remove-home-background",
        help="remove one image from the rotating Home background pool",
    )
    remove_home_background.add_argument("name")
    remove_home_background.add_argument(
        "--yes",
        action="store_true",
        help="remove without interactive confirmation",
    )
    remove_home_background.set_defaults(func=cmd_remove_home_background)

    add_mini = subparsers.add_parser("add-mini", help="import a transparent mini PNG")
    add_mini.add_argument("png")
    add_mini.add_argument("--short-name")
    add_mini.add_argument("--copy")
    add_mini.add_argument("--hat-copy")
    add_mini.add_argument("--notes")
    add_mini.add_argument("--event", action="append")
    add_mini.add_argument("--theme", action="append")
    add_mini.add_argument("--family")
    add_mini.add_argument("--vulgarity", choices=["normal", "brutal"], default="normal")
    add_mini.set_defaults(func=cmd_add_mini)

    remove_mini = subparsers.add_parser(
        "remove-mini",
        help="remove one rejected mini from active assets and content metadata",
    )
    remove_mini.add_argument("asset_id")
    remove_mini.add_argument(
        "--yes",
        action="store_true",
        help="remove without interactive confirmation",
    )
    remove_mini.set_defaults(func=cmd_remove_mini)

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
