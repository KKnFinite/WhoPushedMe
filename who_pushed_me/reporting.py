from __future__ import annotations

from io import BytesIO
from html import escape
from pathlib import Path
from typing import Any, Mapping

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image as ReportImage,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

INK = colors.HexColor("#171916")
CREAM = colors.HexColor("#F1E7C8")
PAPER = colors.HexColor("#F8EFD7")
GREEN = colors.HexColor("#314A3A")
ORANGE = colors.HexColor("#D96B3F")
YELLOW = colors.HexColor("#DFE94B")
MUTED = colors.HexColor("#6B6F68")

ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = (ROOT / "static" / "assets").resolve()


def _safe(value: object) -> str:
    return escape(str(value or ""))


def _participant_name(round_data: Mapping[str, Any], participant_id: object) -> str:
    for participant in round_data.get("participants") or []:
        if str(participant.get("id")) == str(participant_id):
            return str(participant.get("display_name") or "Golfer")
    return "Golfer"


def _route_entries(
    round_data: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return sorted(
        [dict(row) for row in (round_data.get("route") or [])],
        key=lambda row: int(row.get("route_position") or 0),
    )


def _par_map(round_data: Mapping[str, Any]) -> dict[int, int]:
    route_aware = bool(_route_entries(round_data))
    result: dict[int, int] = {}
    for row in round_data.get("pars") or []:
        if row.get("par") is None:
            continue
        key = (
            row.get("route_position")
            if route_aware and row.get("route_position") is not None
            else row.get("hole_number")
        )
        if key is None:
            continue
        result[int(key)] = int(row["par"])
    return result


def _score_map(
    round_data: Mapping[str, Any],
    *,
    participant_id: object | None = None,
) -> dict[int, int]:
    route_aware = bool(_route_entries(round_data))
    result: dict[int, int] = {}
    for row in round_data.get("scores") or []:
        if round_data.get("mode") == "scramble":
            if row.get("score_scope") != "team":
                continue
        else:
            if row.get("score_scope") != "player":
                continue
            if str(row.get("player_participant_id")) != str(participant_id):
                continue
        key = (
            row.get("route_position")
            if route_aware and row.get("route_position") is not None
            else row.get("hole_number")
        )
        if key is None:
            continue
        result[int(key)] = int(row["strokes"])
    return result


def _relative_label(strokes: int | None, par: int | None) -> str:
    if strokes is None or par is None:
        return "-"
    delta = strokes - par
    if delta == 0:
        return "E"
    return f"+{delta}" if delta > 0 else str(delta)


def _rank_label(row: Mapping[str, Any]) -> str:
    rank = row.get("rank")
    if rank is None:
        return "-"
    return f"T{rank}" if int(row.get("tie_count") or 0) > 1 else f"#{rank}"


def _net_rank_label(row: Mapping[str, Any]) -> str:
    rank = row.get("net_rank")
    if rank is None:
        return "-"
    return (
        f"T{rank}"
        if int(row.get("net_tie_count") or 0) > 1
        else f"#{rank}"
    )


def _total_par(round_data: Mapping[str, Any]) -> int | None:
    route = list(round_data.get("route") or [])
    pars = list(round_data.get("pars") or [])

    if route:
        planned = [
            row
            for row in route
            if str(row.get("state") or "planned") != "skipped"
        ]
        if not planned:
            return None
        pars_by_position = {
            int(row["route_position"]): int(row["par"])
            for row in pars
            if (
                row.get("route_position") is not None
                and row.get("par") is not None
            )
        }
        positions = [
            int(row["route_position"])
            for row in planned
        ]
        if any(position not in pars_by_position for position in positions):
            return None
        return sum(pars_by_position[position] for position in positions)

    expected = int(round_data.get("hole_count") or 0)
    if expected < 1 or len(pars) < expected:
        return None
    values = [
        int(row["par"])
        for row in pars
        if row.get("par") is not None
    ]
    if len(values) != expected:
        return None
    return sum(values)


def _net_standings_rows(
    round_data: Mapping[str, Any],
) -> list[list[object]]:
    results = round_data.get("results") or {}
    if not bool(
        round_data.get("net_scoring_enabled")
        or results.get("net_scoring_enabled")
    ):
        return []

    official_net = bool(results.get("net_official"))
    rows: list[list[object]] = [["Net Place", "Golfer", "Hcp", "Net"]]
    players = sorted(
        results.get("players") or [],
        key=lambda row: (
            int(row.get("net_rank") or 999),
            int(row.get("rank") or 999),
            int(row.get("total_strokes") or 9999),
        ),
    )

    for row in players:
        participation = str(row.get("participation_state") or "active")
        coverage = str(
            row.get("coverage_state")
            or (
                "incomplete"
                if int(row.get("missing_scores") or 0)
                else "complete"
            )
        )
        gross_eligible = (
            participation == "active"
            and coverage == "complete"
            and row.get("rank") is not None
        )

        if participation != "active":
            place = "DNF"
        elif coverage == "partial":
            place = "PARTIAL"
        elif coverage != "complete":
            place = "INCOMPLETE"
        elif (
            official_net
            and row.get("net_placement_eligible")
            and row.get("net_rank") is not None
        ):
            place = _net_rank_label(row)
        elif gross_eligible:
            place = "PENDING"
        else:
            place = "-"

        handicap = row.get("round_handicap")
        net_total = row.get("net_total_strokes")
        rows.append(
            [
                place,
                row.get("display_name") or "Golfer",
                (
                    int(handicap)
                    if handicap is not None
                    else "-"
                ),
                (
                    int(net_total)
                    if net_total is not None
                    else "-"
                ),
            ]
        )
    return rows


def _roast_line(
    *,
    total_strokes: int | None,
    total_par: int | None,
    max_vulgarity: str,
) -> str:
    brutal = str(max_vulgarity or "normal") == "brutal"
    if total_strokes is None:
        return "Somehow the scorecard has less evidence than expected."

    if total_par is None:
        if brutal:
            return "No complete par data, so the exact size of the shitshow remains scientifically unverified."
        return "No complete par data, so the exact size of the disaster remains unverified."

    delta = total_strokes - total_par
    if delta <= -1:
        return "Annoyingly competent. We checked the math twice."
    if delta <= 9:
        return (
            "You technically played golf. The witnesses have been informed."
            if not brutal
            else "You technically played golf. Nobody is impressed as hell."
        )
    if delta <= 19:
        return (
            "The scorecard survived. Your dignity had a rougher afternoon."
            if not brutal
            else "The scorecard survived. Your dignity got its ass kicked."
        )
    return (
        "At some point this stopped being golf and became evidence."
        if not brutal
        else "At some point this stopped being golf and became a fucking crime scene."
    )


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "WPMTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=25,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "WPMSubtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=GREEN,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "heading": ParagraphStyle(
            "WPMHeading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=15,
            textColor=GREEN,
            spaceBefore=8,
            spaceAfter=7,
        ),
        "body": ParagraphStyle(
            "WPMBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=INK,
            spaceAfter=5,
        ),
        "roast": ParagraphStyle(
            "WPMRoast",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=INK,
            backColor=YELLOW,
            borderColor=INK,
            borderWidth=1.2,
            borderPadding=8,
            spaceBefore=4,
            spaceAfter=10,
        ),
        "small": ParagraphStyle(
            "WPMSmall",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=MUTED,
        ),
    }


def _table(data: list[list[object]], widths: list[float]) -> Table:
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), GREEN),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("ALIGN", (0, 1), (0, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.65, INK),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [PAPER, CREAM]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _receipt_text(event: Mapping[str, Any]) -> str:
    presentation = event.get("presentation") or {}
    data = event.get("data") or {}
    return str(
        data.get("message")
        or (presentation.get("banter") or {}).get("text")
        or (presentation.get("mascot") or {}).get("copy")
        or (presentation.get("fallback") or {}).get("text")
        or ""
    ).strip()


def _viewer_result(round_data: Mapping[str, Any]) -> dict[str, Any] | None:
    viewer_id = str(round_data.get("viewer_participant_id") or "")
    for row in (round_data.get("results") or {}).get("players") or []:
        if str(row.get("participant_id")) == viewer_id:
            return dict(row)
    return None


def _hole_summary_rows(
    round_data: Mapping[str, Any],
    *,
    participant_id: object | None,
) -> list[list[object]]:
    par_map = _par_map(round_data)
    score_map = _score_map(round_data, participant_id=participant_id)
    rows: list[list[object]] = [["Hole", "Par", "Strokes", "+/-"]]
    route = _route_entries(round_data)

    if route:
        route_length = len(route)
        for entry in route:
            position = int(entry["route_position"])
            hole_number = int(entry["hole_number"])
            label = f"{hole_number} ({position}/{route_length})"
            if str(entry.get("state") or "planned") == "skipped":
                rows.append([label, "-", "-", "UNTRACKED"])
                continue

            par = par_map.get(position)
            strokes = score_map.get(position)
            rows.append(
                [
                    label,
                    par if par is not None else "-",
                    strokes if strokes is not None else "-",
                    _relative_label(strokes, par),
                ]
            )
        return rows

    for hole in range(1, int(round_data.get("hole_count") or 0) + 1):
        par = par_map.get(hole)
        strokes = score_map.get(hole)
        rows.append(
            [
                hole,
                par if par is not None else "-",
                strokes if strokes is not None else "-",
                _relative_label(strokes, par),
            ]
        )
    return rows


def _best_worst_line(
    round_data: Mapping[str, Any],
    *,
    participant_id: object | None,
) -> tuple[str, str]:
    par_map = _par_map(round_data)
    score_map = _score_map(round_data, participant_id=participant_id)
    route = _route_entries(round_data)
    route_by_position = {
        int(row["route_position"]): row
        for row in route
    }

    def label(key: int) -> str:
        entry = route_by_position.get(int(key))
        if not entry:
            return f"#{key}"
        return (
            f"#{int(entry['hole_number'])} "
            f"({int(entry['route_position'])}/{len(route)})"
        )

    candidates: list[tuple[int, int, int]] = []
    for key, strokes in score_map.items():
        par = par_map.get(key)
        if par is not None:
            candidates.append((strokes - par, key, strokes))

    if candidates:
        best = min(candidates, key=lambda item: (item[0], item[1]))
        worst = max(candidates, key=lambda item: (item[0], -item[1]))
        return (
            (
                f"Best hole: {label(best[1])} "
                f"({_relative_label(best[2], par_map[best[1]])})"
            ),
            (
                f"Worst hole: {label(worst[1])} "
                f"({_relative_label(worst[2], par_map[worst[1]])})"
            ),
        )

    if score_map:
        best_key = min(
            score_map,
            key=lambda key: (score_map[key], key),
        )
        worst_key = max(
            score_map,
            key=lambda key: (score_map[key], -key),
        )
        return (
            f"Lowest stroke hole: {label(best_key)} ({score_map[best_key]})",
            f"Highest stroke hole: {label(worst_key)} ({score_map[worst_key]})",
        )

    return ("Best hole: unavailable", "Worst hole: unavailable")


def _content_archive_entries(
    round_data: Mapping[str, Any],
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    for event in reversed(list(round_data.get("events") or [])):
        presentation = event.get("presentation") or {}
        banter = presentation.get("banter") or {}
        mascot = presentation.get("mascot") or {}
        data = event.get("data") or {}

        custom_message = str(data.get("message") or "").strip()
        banter_text = str(banter.get("text") or "").strip()
        mascot_copy = str(mascot.get("copy") or "").strip()
        mascot_path = str(mascot.get("production") or "").strip()

        if not (custom_message or banter_text or mascot_copy or mascot_path):
            continue

        entries.append(
            {
                "event_type": str(event.get("event_type") or ""),
                "event_key": str(event.get("content_event_key") or ""),
                "hole_number": event.get("hole_number"),
                "created_at": event.get("created_at"),
                "custom_message": custom_message,
                "banter_text": banter_text,
                "mascot_copy": mascot_copy,
                "mascot_path": mascot_path,
            }
        )

    return entries


def _asset_file(value: object) -> Path | None:
    relative = str(value or "").strip().lstrip("/")
    if not relative:
        return None

    candidate = (ROOT / relative).resolve()
    if ASSET_ROOT != candidate and ASSET_ROOT not in candidate.parents:
        return None
    if not candidate.is_file():
        return None
    return candidate


def _mini_image(value: object) -> ReportImage | None:
    path = _asset_file(value)
    if path is None:
        return None

    try:
        image = ReportImage(str(path))
    except Exception:
        return None

    max_width = 0.95 * inch
    max_height = 1.05 * inch
    width = float(image.imageWidth or max_width)
    height = float(image.imageHeight or max_height)
    scale = min(max_width / width, max_height / height)
    image.drawWidth = width * scale
    image.drawHeight = height * scale
    return image


def _append_content_archive(
    story: list[Any],
    round_data: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
) -> None:
    entries = _content_archive_entries(round_data)
    if not entries:
        return

    story.append(Paragraph("FULL TRASH-TALK & MINI ARCHIVE", styles["heading"]))
    story.append(
        Paragraph(
            (
                "Every banter line and mini mascot actually selected during this "
                "round is preserved below. If the same insult fired twice, it stays "
                "twice. Evidence is evidence."
            ),
            styles["body"],
        )
    )

    for entry in entries:
        meta_parts: list[str] = []
        if entry["hole_number"] is not None:
            meta_parts.append(f"HOLE {entry['hole_number']}")
        if entry["event_key"]:
            meta_parts.append(str(entry["event_key"]))
        elif entry["event_type"]:
            meta_parts.append(str(entry["event_type"]))

        text_flowables: list[Any] = []
        if meta_parts:
            text_flowables.append(
                Paragraph(_safe(" | ".join(meta_parts)), styles["small"])
            )

        if entry["custom_message"]:
            text_flowables.append(
                Paragraph(
                    f"<b>CUSTOM:</b> {_safe(entry['custom_message'])}",
                    styles["body"],
                )
            )

        if entry["banter_text"]:
            text_flowables.append(
                Paragraph(
                    f"<b>BANTER:</b> {_safe(entry['banter_text'])}",
                    styles["body"],
                )
            )

        if entry["mascot_copy"]:
            text_flowables.append(
                Paragraph(
                    f"<b>MINI:</b> {_safe(entry['mascot_copy'])}",
                    styles["body"],
                )
            )

        mini = _mini_image(entry["mascot_path"])
        left_cell: Any = mini if mini is not None else ""
        right_cell: Any = text_flowables or [
            Paragraph("Presentation recorded.", styles["small"])
        ]

        row = Table(
            [[left_cell, right_cell]],
            colWidths=[1.1 * inch, 5.25 * inch],
            hAlign="LEFT",
        )
        row.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                    ("BOX", (0, 0), (-1, -1), 0.8, INK),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.append(row)
        story.append(Spacer(1, 0.07 * inch))


def _append_individual(
    story: list[Any],
    round_data: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
    *,
    preferences: Mapping[str, Any],
) -> None:
    results = (round_data.get("results") or {}).get("players") or []
    total_par = _total_par(round_data)
    viewer = _viewer_result(round_data)
    viewer_id = round_data.get("viewer_participant_id")
    is_player = str(round_data.get("viewer_role")) == "player" and viewer is not None

    if is_player:
        coverage = str(
            viewer.get("coverage_state")
            or ("incomplete" if int(viewer.get("missing_scores") or 0) else "complete")
        )
        participation = str(viewer.get("participation_state") or "active")
        official = (
            participation == "active"
            and coverage == "complete"
            and viewer.get("rank") is not None
        )
        title = f"{viewer.get('display_name') or 'Golfer'} - Final Damage Report"
        story.append(Paragraph(_safe(title), styles["heading"]))

        if official:
            total_strokes = int(viewer.get("total_strokes") or 0)
            story.append(
                Paragraph(
                    _safe(
                        _roast_line(
                            total_strokes=total_strokes,
                            total_par=total_par,
                            max_vulgarity=str(preferences.get("max_vulgarity") or "normal"),
                        )
                    ),
                    styles["roast"],
                )
            )
            summary = (
                f"Final position: {_rank_label(viewer)} | "
                f"{total_strokes} strokes | "
                f"{_relative_label(total_strokes, total_par)} to par"
                if total_par is not None
                else f"Final position: {_rank_label(viewer)} | {total_strokes} strokes"
            )
        else:
            if participation != "active":
                status_label = "DNF"
            elif coverage == "partial":
                status_label = "PARTIAL"
            else:
                status_label = "INCOMPLETE"
            story.append(
                Paragraph(
                    "The scorecard closed with missing evidence. No fake final total was invented.",
                    styles["roast"],
                )
            )
            score_count = int(viewer.get("score_count") or 0)
            required = int(viewer.get("required_scores") or 0)
            summary = (
                f"Status: {status_label} | "
                f"{score_count} of {required} required scores recorded"
                if required
                else f"Status: {status_label} | {score_count} scores recorded"
            )

        if (
            official
            and bool(
                round_data.get("net_scoring_enabled")
                or (round_data.get("results") or {}).get(
                    "net_scoring_enabled"
                )
            )
        ):
            round_handicap = viewer.get("round_handicap")
            net_total = viewer.get("net_total_strokes")
            if round_handicap is None:
                summary += " | Net pending handicap"
            elif net_total is not None:
                summary += (
                    f" | Hcp {int(round_handicap)}"
                    f" | {int(net_total)} net"
                )
                if (
                    (round_data.get("results") or {}).get("net_official")
                    and viewer.get("net_rank") is not None
                ):
                    summary += (
                        f" | Net position: {_net_rank_label(viewer)}"
                    )

        story.append(Paragraph(_safe(summary), styles["body"]))
        best, worst = _best_worst_line(
            round_data,
            participant_id=viewer_id,
        )
        story.append(Paragraph(_safe(f"{best} | {worst}"), styles["body"]))

        story.append(Paragraph("YOUR HOLE-BY-HOLE EVIDENCE", styles["heading"]))
        story.append(
            _table(
                _hole_summary_rows(round_data, participant_id=viewer_id),
                [1.1 * inch, 0.75 * inch, 1.0 * inch, 0.8 * inch],
            )
        )

    story.append(Paragraph("FINAL GROSS STANDINGS", styles["heading"]))
    standings = [["Place", "Golfer", "Strokes", "To Par"]]
    for row in sorted(
        results,
        key=lambda item: (
            int(item.get("rank") or 999),
            int(item.get("total_strokes") or 9999),
        ),
    ):
        coverage = str(
            row.get("coverage_state")
            or ("incomplete" if int(row.get("missing_scores") or 0) else "complete")
        )
        participation = str(row.get("participation_state") or "active")
        official = (
            participation == "active"
            and coverage == "complete"
            and row.get("rank") is not None
        )
        if official:
            strokes = int(row.get("total_strokes") or 0)
            place = _rank_label(row)
            relative = _relative_label(strokes, total_par)
            strokes_cell: object = strokes
        else:
            place = (
                "DNF"
                if participation != "active"
                else "PARTIAL"
                if coverage == "partial"
                else "INCOMPLETE"
            )
            strokes_cell = "-"
            relative = "-"
        standings.append(
            [
                place,
                row.get("display_name") or "Golfer",
                strokes_cell,
                relative,
            ]
        )
    story.append(
        _table(
            standings,
            [0.65 * inch, 2.7 * inch, 0.85 * inch, 0.75 * inch],
        )
    )

    net_rows = _net_standings_rows(round_data)
    if net_rows:
        story.append(Paragraph("NET STANDINGS", styles["heading"]))
        story.append(
            Paragraph(
                (
                    "Net placement is official only when every gross-placement-"
                    "eligible golfer has a round handicap."
                ),
                styles["small"],
            )
        )
        story.append(
            _table(
                net_rows,
                [0.85 * inch, 2.65 * inch, 0.75 * inch, 0.85 * inch],
            )
        )


def _append_scramble(
    story: list[Any],
    round_data: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
    *,
    preferences: Mapping[str, Any],
) -> None:
    results = round_data.get("results") or {}
    complete = bool(results.get("complete"))
    total = results.get("team_total")
    total_strokes = int(total) if total is not None else None
    total_par = _total_par(round_data)

    if complete:
        story.append(Paragraph("TEAM FINAL DAMAGE REPORT", styles["heading"]))
        story.append(
            Paragraph(
                _safe(
                    _roast_line(
                        total_strokes=total_strokes,
                        total_par=total_par,
                        max_vulgarity=str(preferences.get("max_vulgarity") or "normal"),
                    )
                ),
                styles["roast"],
            )
        )
        summary = (
            f"{total_strokes} team strokes"
            if total_strokes is not None
            else "Team total unavailable"
        )
        if total_strokes is not None and total_par is not None:
            summary += f" | {_relative_label(total_strokes, total_par)} to par"
    else:
        story.append(Paragraph("INCOMPLETE ROUND", styles["heading"]))
        story.append(
            Paragraph(
                "The round ended with missing team scores. No fake final total was invented.",
                styles["roast"],
            )
        )
        score_count = int(results.get("score_count") or 0)
        required = int(results.get("required_scores") or round_data.get("hole_count") or 0)
        missing = int(results.get("missing_scores") or max(required - score_count, 0))
        summary = (
            f"{score_count} of {required} team scores recorded | "
            f"{missing} missing"
        )
    story.append(Paragraph(_safe(summary), styles["body"]))

    best, worst = _best_worst_line(round_data, participant_id=None)
    story.append(Paragraph(_safe(f"{best} | {worst}"), styles["body"]))

    story.append(Paragraph("TEAM HOLE-BY-HOLE EVIDENCE", styles["heading"]))
    story.append(
        _table(
            _hole_summary_rows(round_data, participant_id=None),
            [1.1 * inch, 0.75 * inch, 1.0 * inch, 0.8 * inch],
        )
    )

    players = {
        str(row.get("id")): str(row.get("display_name") or "Golfer")
        for row in round_data.get("participants") or []
        if row.get("role") == "player"
    }
    counts = {participant_id: 0 for participant_id in players}
    shot_types: dict[str, set[str]] = {participant_id: set() for participant_id in players}

    for contribution in round_data.get("contributions") or []:
        participant_id = str(contribution.get("player_participant_id") or "")
        if participant_id not in counts:
            continue
        counts[participant_id] += 1
        shot_types[participant_id].add(str(contribution.get("shot_type") or "").replace("_", " "))

    story.append(Paragraph("CONTRIBUTION AUDIT", styles["heading"]))
    rows: list[list[object]] = [["Golfer", "Selected shots", "What they got credit for"]]
    for participant_id, name in players.items():
        rows.append(
            [
                name,
                counts[participant_id],
                ", ".join(sorted(shot_types[participant_id])) or "-",
            ]
        )
    story.append(_table(rows, [2.0 * inch, 1.0 * inch, 3.1 * inch]))


def build_round_report_pdf(
    round_data: Mapping[str, Any],
    *,
    preferences: Mapping[str, Any] | None = None,
) -> bytes:
    if str(round_data.get("status")) != "completed":
        raise ValueError("round must be completed before generating a final report")

    prefs = dict(preferences or {})
    styles = _styles()
    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
        title="Who Pushed Me?! Final Damage Report",
        author="Who Pushed Me?!",
        subject="Golf round final damage report",
    )

    place = (
        (round_data.get("course") or {}).get("name")
        or round_data.get("free_play_name")
        or "Unknown Course"
    )

    story: list[Any] = [
        Paragraph("WHO PUSHED ME?!", styles["title"]),
        Paragraph(
            "FINAL DAMAGE REPORT - SCORE GOLF. BLAME FRIENDS.",
            styles["subtitle"],
        ),
        Paragraph(
            _safe(
                f"{place} | {round_data.get('hole_count')} holes | "
                f"{'Scramble' if round_data.get('mode') == 'scramble' else 'Individual'}"
            ),
            styles["body"],
        ),
        Spacer(1, 0.08 * inch),
    ]

    if round_data.get("mode") == "scramble":
        _append_scramble(story, round_data, styles, preferences=prefs)
    else:
        _append_individual(story, round_data, styles, preferences=prefs)

    _append_content_archive(story, round_data, styles)

    story.extend(
        [
            Spacer(1, 0.12 * inch),
            KeepTogether(
                [
                    Paragraph(
                        "OFFICIAL CONCLUSION",
                        styles["heading"],
                    ),
                    Paragraph(
                        "This document is a factual score summary wrapped in the level of disrespect the round earned.",
                        styles["body"],
                    ),
                    Paragraph(
                        "Generated by WHO PUSHED ME?! Scorecard.",
                        styles["small"],
                    ),
                ]
            ),
        ]
    )

    document.build(story)
    return output.getvalue()
