from __future__ import annotations

import json
import random
from pathlib import Path
from string import Formatter
from typing import Any, Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = Path(__file__).resolve().parent
ASSET_MANIFEST = ROOT / "static" / "assets" / "_meta" / "asset-manifest.json"

VULGARITY_ORDER = {"normal": 0, "brutal": 1}
AUDIT_STATUSES = {"pending", "verified"}
ALLOWED_AUDIENCES = {"everyone", "actor", "target", "subject", "others", "team"}
ALLOWED_PLACEHOLDERS = {
    "actor",
    "target",
    "subject",
    "hole",
    "par",
    "strokes",
    "score_name",
    "old_score",
    "new_score",
    "mode",
    "course",
}


class ContentError(ValueError):
    """Raised when content metadata or event configuration is invalid."""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class EventRegistry:
    def __init__(self, data: Mapping[str, Any]) -> None:
        self.schema_version = int(data.get("schema_version", 0))
        self.aliases = dict(data.get("aliases") or {})
        self.asset_families = dict(data.get("asset_families") or {})
        rows = list(data.get("events") or [])
        self.events = {row["key"]: dict(row) for row in rows}
        self.validate()

    @classmethod
    def load(cls, path: Path | None = None) -> "EventRegistry":
        return cls(_read_json(path or CONTENT_DIR / "events.json"))

    def validate(self) -> None:
        if self.schema_version != 1:
            raise ContentError("unsupported events schema_version")
        if len(self.events) == 0:
            raise ContentError("event registry is empty")

        for key, event in self.events.items():
            if event.get("key") != key:
                raise ContentError(f"event key mismatch for {key}")
            parent = event.get("parent")
            if parent is not None and parent not in self.events:
                raise ContentError(f"event {key} has unknown parent {parent}")
            audiences = set(event.get("audiences") or ["everyone"])
            unknown = audiences - ALLOWED_AUDIENCES
            if unknown:
                raise ContentError(f"event {key} has unknown audiences: {sorted(unknown)}")
            family = event.get("asset_family")
            if family and family not in self.asset_families:
                raise ContentError(f"event {key} uses unknown asset_family {family}")

        for alias, target in self.aliases.items():
            if target not in self.events:
                raise ContentError(f"alias {alias} targets unknown event {target}")

        for key in self.events:
            self.lineage(key)

    def canonical_key(self, key: str) -> str:
        candidate = self.aliases.get(key, key)
        if candidate not in self.events:
            raise ContentError(f"unknown event key: {key}")
        return candidate

    def event(self, key: str) -> dict[str, Any]:
        return self.events[self.canonical_key(key)]

    def lineage(self, key: str) -> list[str]:
        current = self.canonical_key(key)
        seen: set[str] = set()
        lineage: list[str] = []
        while current is not None:
            if current in seen:
                raise ContentError(f"event parent cycle detected at {current}")
            seen.add(current)
            lineage.append(current)
            parent = self.events[current].get("parent")
            current = parent
        return lineage

    def is_enabled(
        self,
        key: str,
        overrides: Mapping[str, bool] | None = None,
    ) -> bool:
        overrides = overrides or {}
        canonical_overrides = {
            self.canonical_key(event_key): bool(enabled)
            for event_key, enabled in overrides.items()
        }
        for event_key in self.lineage(key):
            if event_key in canonical_overrides:
                if not canonical_overrides[event_key]:
                    return False
                continue
            if not bool(self.events[event_key].get("default_enabled", True)):
                return False
        return True

    def asset_family(self, key: str) -> str | None:
        for event_key in self.lineage(key):
            family = self.events[event_key].get("asset_family")
            if family:
                return str(family)
        return None

    def selectable_events(self, *, include_scopes: bool = True) -> list[dict[str, Any]]:
        rows = []
        for key in sorted(self.events):
            event = self.events[key]
            if key.startswith("generic."):
                continue
            if include_scopes or event.get("triggerable"):
                rows.append(event)
        return rows


class ContentCatalog:
    def __init__(
        self,
        registry: EventRegistry,
        themes: Mapping[str, Any],
        banter: Mapping[str, Any],
        mascots: Mapping[str, Any],
        asset_manifest: Mapping[str, Any],
    ) -> None:
        self.registry = registry
        self.theme_rows = list(themes.get("themes") or [])
        self.themes = {row["key"]: dict(row) for row in self.theme_rows}
        self.banter = list(banter.get("banter") or [])
        self.mascots = list(mascots.get("mascots") or [])
        self.asset_manifest = dict(asset_manifest)

    @classmethod
    def load(cls) -> "ContentCatalog":
        return cls(
            EventRegistry.load(),
            _read_json(CONTENT_DIR / "themes.json"),
            _read_json(CONTENT_DIR / "banter.json"),
            _read_json(CONTENT_DIR / "mascots.json"),
            _read_json(ASSET_MANIFEST),
        )

    def validate(self, *, strict_mascot_audit: bool = False) -> None:
        errors: list[str] = []

        if len(self.themes) != len(self.theme_rows):
            errors.append("duplicate theme key")

        asset_rows = list(self.asset_manifest.get("assets") or [])
        mini_assets = {
            row["asset_id"]
            for row in asset_rows
            if row.get("family") == "mini-mascot"
        }

        seen_banter: set[str] = set()
        for row in self.banter:
            content_id = str(row.get("id") or "")
            if not content_id:
                errors.append("banter entry missing id")
                continue
            if content_id in seen_banter:
                errors.append(f"duplicate banter id {content_id}")
            seen_banter.add(content_id)
            errors.extend(self._validate_content_row(row, content_id, has_text=True))

        seen_mascots: set[str] = set()
        for row in self.mascots:
            asset_id = str(row.get("asset_id") or "")
            if not asset_id:
                errors.append("mascot entry missing asset_id")
                continue
            if asset_id in seen_mascots:
                errors.append(f"duplicate mascot asset_id {asset_id}")
            seen_mascots.add(asset_id)
            if asset_id not in mini_assets:
                errors.append(f"mascot metadata references unknown mini asset {asset_id}")
            errors.extend(self._validate_content_row(row, asset_id, has_text=False))
            errors.extend(
                self._validate_mascot_metadata(
                    row,
                    asset_id,
                    strict_audit=strict_mascot_audit,
                )
            )

        missing_metadata = sorted(mini_assets - seen_mascots)
        extra_metadata = sorted(seen_mascots - mini_assets)
        if missing_metadata:
            errors.append(f"mini assets missing content metadata: {missing_metadata}")
        if extra_metadata:
            errors.append(f"content metadata without mini asset: {extra_metadata}")

        if errors:
            raise ContentError("\n".join(errors))

    def _validate_mascot_metadata(
        self,
        row: Mapping[str, Any],
        asset_id: str,
        *,
        strict_audit: bool,
    ) -> list[str]:
        errors: list[str] = []

        audit_status = str(row.get("audit_status") or "")
        if audit_status not in AUDIT_STATUSES:
            errors.append(
                f"{asset_id} has invalid audit_status {audit_status or '<missing>'}"
            )

        copy = row.get("copy")
        if copy is not None and not isinstance(copy, str):
            errors.append(f"{asset_id} copy must be a string or null")

        signs = row.get("signs")
        if not isinstance(signs, list) or not all(
            isinstance(value, str) for value in signs
        ):
            errors.append(f"{asset_id} signs must be a list of strings")

        hat_copy = row.get("hat_copy")
        if hat_copy is not None and not isinstance(hat_copy, str):
            errors.append(f"{asset_id} hat_copy must be a string or null")

        notes = row.get("notes")
        if notes is not None and not isinstance(notes, str):
            errors.append(f"{asset_id} notes must be a string")

        if audit_status == "verified":
            if not str(copy or "").strip():
                errors.append(f"{asset_id} verified mascot is missing exact copy")
            if not signs:
                errors.append(f"{asset_id} verified mascot is missing sign panels")

        if strict_audit and audit_status != "verified":
            errors.append(f"{asset_id} has not been visually audited")

        return errors

    def mascot_audit_summary(self) -> dict[str, int]:
        summary = {status: 0 for status in sorted(AUDIT_STATUSES)}
        for row in self.mascots:
            status = str(row.get("audit_status") or "pending")
            summary[status] = summary.get(status, 0) + 1
        return summary

    def _validate_content_row(
        self,
        row: Mapping[str, Any],
        content_id: str,
        *,
        has_text: bool,
    ) -> list[str]:
        errors: list[str] = []
        events = list(row.get("events") or [])
        if not events:
            errors.append(f"{content_id} has no eligible events")
        for event_key in events:
            try:
                self.registry.canonical_key(str(event_key))
            except ContentError as error:
                errors.append(f"{content_id}: {error}")

        vulgarity = str(row.get("vulgarity") or "normal")
        if vulgarity not in VULGARITY_ORDER:
            errors.append(f"{content_id} has invalid vulgarity {vulgarity}")

        for theme in row.get("themes") or []:
            if theme not in self.themes:
                errors.append(f"{content_id} uses unknown theme {theme}")

        audiences = set(row.get("audiences") or ["everyone"])
        unknown_audiences = audiences - ALLOWED_AUDIENCES
        if unknown_audiences:
            errors.append(
                f"{content_id} uses unknown audiences {sorted(unknown_audiences)}"
            )

        if has_text:
            text = str(row.get("text") or "")
            if not text:
                errors.append(f"{content_id} has empty text")
            for _, field_name, _, _ in Formatter().parse(text):
                if field_name and field_name not in ALLOWED_PLACEHOLDERS:
                    errors.append(
                        f"{content_id} uses unsupported placeholder {{{field_name}}}"
                    )
        return errors

    def _eligible(
        self,
        rows: Sequence[Mapping[str, Any]],
        event_key: str,
        *,
        audience: str = "everyone",
        admin_overrides: Mapping[str, bool] | None = None,
        max_vulgarity: str | None = None,
        blocked_themes: Iterable[str] = (),
    ) -> list[dict[str, Any]]:
        canonical = self.registry.canonical_key(event_key)
        if not self.registry.is_enabled(canonical, admin_overrides):
            return []
        if audience not in ALLOWED_AUDIENCES:
            raise ContentError(f"unknown audience: {audience}")
        if max_vulgarity is not None and max_vulgarity not in VULGARITY_ORDER:
            raise ContentError(f"unknown vulgarity level: {max_vulgarity}")

        lineage = self.registry.lineage(canonical)
        positions = {value: index for index, value in enumerate(lineage)}
        blocked = set(blocked_themes)
        ranked: list[tuple[int, dict[str, Any]]] = []

        for source_row in rows:
            row = dict(source_row)
            if not bool(row.get("enabled", True)):
                continue

            audiences = set(row.get("audiences") or ["everyone"])
            if "everyone" not in audiences and audience not in audiences:
                continue

            vulgarity = str(row.get("vulgarity") or "normal")
            if (
                max_vulgarity is not None
                and VULGARITY_ORDER[vulgarity] > VULGARITY_ORDER[max_vulgarity]
            ):
                continue

            if blocked.intersection(row.get("themes") or []):
                continue

            matched_positions = []
            for content_event in row.get("events") or []:
                candidate = self.registry.canonical_key(str(content_event))
                if candidate in positions:
                    matched_positions.append(positions[candidate])
            if not matched_positions:
                continue
            ranked.append((min(matched_positions), row))

        if not ranked:
            return []

        best_rank = min(rank for rank, _ in ranked)
        return [row for rank, row in ranked if rank == best_rank]

    def eligible_banter(self, event_key: str, **kwargs: Any) -> list[dict[str, Any]]:
        return self._eligible(self.banter, event_key, **kwargs)

    def eligible_mascots(self, event_key: str, **kwargs: Any) -> list[dict[str, Any]]:
        return self._eligible(self.mascots, event_key, **kwargs)

    def choose_banter(
        self,
        event_key: str,
        *,
        rng: random.Random | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        choices = self.eligible_banter(event_key, **kwargs)
        return (rng or random).choice(choices) if choices else None

    def choose_mascot(
        self,
        event_key: str,
        *,
        rng: random.Random | None = None,
        **kwargs: Any,
    ) -> dict[str, Any] | None:
        choices = self.eligible_mascots(event_key, **kwargs)
        return (rng or random).choice(choices) if choices else None

    def render_banter(
        self,
        row: Mapping[str, Any],
        context: Mapping[str, object],
    ) -> str:
        try:
            return str(row["text"]).format_map(dict(context))
        except KeyError as error:
            raise ContentError(
                f"missing banter placeholder value: {error.args[0]}"
            ) from error
