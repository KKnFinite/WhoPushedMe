from __future__ import annotations

from io import BytesIO
from html import escape
from typing import Any, Mapping

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
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


def _safe(value: object) -> str:
    return escape(str(value or ""))


def _participant_name(round_data: Mapping[str, Any], participant_id: object) -> str:
    for participant in round_data.get("participants") or []:
        if str(participant.get("id")) == str(participant_id):
            return str(participant.get("display_name") or "Golfer")
    return "Golfer"


def _par_map(round_data: Mapping[str, Any]) -> dict[int, int]:
    return {
        int(row["hole_number"]): int(row["par"])
        for row in round_data.get("pars") or []
        if row.get("par") is not None
    }


def _score_map(
    round_data: Mapping[str, Any],
    *,
    participant_id: object | None = None,
) -> dict[int, int]:
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
        result[int(row["hole_number"])] = int(row["strokes"])
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
    candidates: list[tuple[int, int, int]] = []
    for hole, strokes in score_map.items():
        par = par_map.get(hole)
        if par is not None:
            candidates.append((strokes - par, hole, strokes))

    if candidates:
        best = min(candidates, key=lambda item: (item[0], item[1]))
        worst = max(candidates, key=lambda item: (item[0], -item[1]))
        return (
            f"Best hole: #{best[1]} ({_relative_label(best[2], par_map[best[1]])})",
            f"Worst hole: #{worst[1]} ({_relative_label(worst[2], par_map[worst[1]])})",
        )

    if score_map:
        best_hole = min(score_map, key=lambda hole: (score_map[hole], hole))
        worst_hole = max(score_map, key=lambda hole: (score_map[hole], -hole))
        return (
            f"Lowest stroke hole: #{best_hole} ({score_map[best_hole]})",
            f"Highest stroke hole: #{worst_hole} ({score_map[worst_hole]})",
        )

    return ("Best hole: unavailable", "Worst hole: unavailable")


def _append_receipts(story: list[Any], round_data: Mapping[str, Any], styles: dict[str, ParagraphStyle]) -> None:
    receipts: list[str] = []
    for event in round_data.get("events") or []:
        text = _receipt_text(event)
        if text and text not in receipts:
            receipts.append(text)
        if len(receipts) >= 8:
            break

    if not receipts:
        return

    story.append(Paragraph("SELECTED RECEIPTS", styles["heading"]))
    for text in receipts:
        story.append(Paragraph(f"- {_safe(text)}", styles["body"]))


def _append_individual(
    story: list[Any],
    round_data: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
    *,
    preferences: Mapping[str, Any],
) -> None:
    results = (round_data.get("results") or {}).get("players") or []
    total_par = (
        sum(_par_map(round_data).values())
        if len(_par_map(round_data)) == int(round_data.get("hole_count") or 0)
        else None
    )
    viewer = _viewer_result(round_data)
    viewer_id = round_data.get("viewer_participant_id")
    is_player = str(round_data.get("viewer_role")) == "player" and viewer is not None

    if is_player:
        total_strokes = int(viewer.get("total_strokes") or 0)
        title = f"{viewer.get('display_name') or 'Golfer'} - Final Damage Report"
        story.append(Paragraph(_safe(title), styles["heading"]))
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
        best, worst = _best_worst_line(
            round_data,
            participant_id=viewer_id,
        )
        story.append(
            Paragraph(
                _safe(
                    f"Final position: {_rank_label(viewer)} | "
                    f"{total_strokes} strokes | "
                    f"{_relative_label(total_strokes, total_par)} to par"
                    if total_par is not None
                    else f"Final position: {_rank_label(viewer)} | {total_strokes} strokes"
                ),
                styles["body"],
            )
        )
        story.append(Paragraph(_safe(f"{best} | {worst}"), styles["body"]))

        story.append(Paragraph("YOUR HOLE-BY-HOLE EVIDENCE", styles["heading"]))
        story.append(
            _table(
                _hole_summary_rows(round_data, participant_id=viewer_id),
                [0.75 * inch, 0.75 * inch, 1.0 * inch, 0.8 * inch],
            )
        )

    story.append(Paragraph("FINAL STANDINGS", styles["heading"]))
    standings = [["Place", "Golfer", "Strokes", "To Par"]]
    for row in sorted(
        results,
        key=lambda item: (
            int(item.get("rank") or 999),
            int(item.get("total_strokes") or 9999),
        ),
    ):
        strokes = int(row.get("total_strokes") or 0)
        standings.append(
            [
                _rank_label(row),
                row.get("display_name") or "Golfer",
                strokes,
                _relative_label(strokes, total_par),
            ]
        )
    story.append(_table(standings, [0.65 * inch, 2.7 * inch, 0.85 * inch, 0.75 * inch]))


def _append_scramble(
    story: list[Any],
    round_data: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
    *,
    preferences: Mapping[str, Any],
) -> None:
    total = (round_data.get("results") or {}).get("team_total")
    total_strokes = int(total) if total is not None else None
    par_map = _par_map(round_data)
    total_par = (
        sum(par_map.values())
        if len(par_map) == int(round_data.get("hole_count") or 0)
        else None
    )

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

    summary = f"{total_strokes} team strokes" if total_strokes is not None else "Team total unavailable"
    if total_strokes is not None and total_par is not None:
        summary += f" | {_relative_label(total_strokes, total_par)} to par"
    story.append(Paragraph(_safe(summary), styles["body"]))

    best, worst = _best_worst_line(round_data, participant_id=None)
    story.append(Paragraph(_safe(f"{best} | {worst}"), styles["body"]))

    story.append(Paragraph("TEAM HOLE-BY-HOLE EVIDENCE", styles["heading"]))
    story.append(
        _table(
            _hole_summary_rows(round_data, participant_id=None),
            [0.75 * inch, 0.75 * inch, 1.0 * inch, 0.8 * inch],
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

    _append_receipts(story, round_data, styles)

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
