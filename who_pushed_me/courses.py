from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CourseHole:
    number: int
    par: int | None
    stroke_index: int | None
    tee_yardages: dict[str, int]


@dataclass(frozen=True)
class CourseSnapshot:
    external_id: str
    name: str
    holes: tuple[CourseHole, ...]


class CourseProvider(Protocol):
    def search(self, query: str, *, limit: int = 10) -> list[dict[str, object]]: ...

    def fetch(self, external_id: str) -> CourseSnapshot: ...


class OpenGolfAPI:
    """Small adapter around the read-only OpenGolfAPI course endpoints."""

    def __init__(
        self,
        *,
        base_url: str = "https://api.opengolfapi.org/v1",
        api_key: str | None = None,
        timeout_seconds: float = 8.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def _get(self, path: str, query: dict[str, object] | None = None) -> dict[str, object]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{urlencode(query)}"
        headers = {"Accept": "application/json", "User-Agent": "WhoPushedMe/0.3"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = Request(url, headers=headers)
        with urlopen(request, timeout=self.timeout_seconds) as response:
            return json.load(response)

    def search(self, query: str, *, limit: int = 10) -> list[dict[str, object]]:
        search = str(query or "").strip()
        if len(search) < 2:
            return []

        payload = self._get(
            "courses/search",
            {"q": search, "limit": max(1, min(limit, 25))},
        )
        courses = payload.get("courses", [])
        if not isinstance(courses, list):
            return []

        results: list[dict[str, object]] = []
        for raw in courses:
            if not isinstance(raw, dict):
                continue
            external_id = raw.get("id") or raw.get("course_id")
            name = raw.get("name") or raw.get("course_name")
            if external_id is None or not name:
                continue

            item: dict[str, object] = {
                "external_course_id": str(external_id),
                "name": str(name),
            }
            for source_key, target_key in (
                ("city", "city"),
                ("state", "state"),
                ("state_province", "state"),
                ("country", "country"),
            ):
                if raw.get(source_key) and target_key not in item:
                    item[target_key] = str(raw[source_key])
            results.append(item)

        return results

    def fetch(self, external_id: str) -> CourseSnapshot:
        safe_id = quote(str(external_id), safe="")
        detail = self._get(f"courses/{safe_id}")
        holes_payload = self._get(f"courses/{safe_id}/holes")
        course = detail.get("course", detail)
        if not isinstance(course, dict):
            course = detail
        holes: list[CourseHole] = []
        for raw_hole in holes_payload.get("holes", []):
            if not isinstance(raw_hole, dict):
                continue
            raw_yardages = raw_hole.get("yardages") or {}
            yardages = {
                str(tee): int(yards)
                for tee, yards in raw_yardages.items()
                if yards is not None and int(yards) > 0
            }
            holes.append(
                CourseHole(
                    number=int(raw_hole["number"]),
                    par=int(raw_hole["par"]) if raw_hole.get("par") is not None else None,
                    stroke_index=(
                        int(raw_hole["handicap_index"])
                        if raw_hole.get("handicap_index") is not None
                        else None
                    ),
                    tee_yardages=yardages,
                )
            )
        return CourseSnapshot(
            external_id=str(course.get("id", external_id)),
            name=str(course.get("name") or course.get("course_name") or external_id),
            holes=tuple(holes),
        )
